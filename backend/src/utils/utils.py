from autogluon.tabular import TabularPredictor
from sklearn.ensemble import VotingClassifier
from sklearn.base import BaseEstimator, ClassifierMixin
from lightgbm import LGBMClassifier
from lightgbm import basic 
import numpy as np
import warnings
import torch
import re
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, TransformerMixin
import mlflow
def extract_layers_as_nested_dict(model_str):
    """
    Parses a model string and returns a nested dictionary representing the model's layer hierarchy.
    """
    lines = model_str.strip().split('\n')
    root = {}
    stack = [(0, root)]

    for line in lines:
        #print(line)
        #print(root)
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip())
        content = line.strip()

        # Match a layer line: (name): description
        match = re.match(r'(\(?\w+\)?):\s+(.+)', content)
        
        #print(match)
        if match:
            #print(f"Match found: {match.groups()}")
            name, desc = match.groups()
            node = {}
            # Adjust the stack to the current indentation level
            while stack and indent <= stack[-1][0]:
                stack.pop()
            # Add the node to the current parent
            parent = stack[-1][1]
            parent[name] = {'_desc': desc}
            # Push this node onto the stack as the new parent
            stack.append((indent, parent[name]))
        else:
            # If line doesn't match layer pattern (e.g., TabularModel(), etc.), ignore
            continue

    return root

class PlaceholderTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, desc="PassThrough"):
        self.desc = desc
        match = re.match(r'^(\w+)\((.*)\)$', desc)
        # print(f"Processing description: {desc}")
        # print(f"Match result: {match}")
        if match:
            # If the description matches a function call pattern, extract the class name
            self.class_name, self.desc = match.groups()
        else:
            # Otherwise, assume it's just a class name
            self.class_name = desc        
        # Set the class name dynamically to match the description
        # print(f"Class name set to: {self.class_name}")

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X
    

    def __sklearn_is_fitted__(self):
        # Bypass sklearn's is_fitted check
        # since AutoGluon models don't follow sklearn's conventions.
        return True 

    def __repr__(self):
        # return f"PlaceholderTransformer(desc='{self.desc}')"
        # self.__class__.__name__ = self.class_name
        return f'{self.__class__.__name__}({self.desc})'

class RenamedPipeline(Pipeline):
    """
    A custom Pipeline class that allows dynamic renaming of the class name
    based on the description provided.
    """
    def __init__(self, steps, memory=None, verbose=False, class_name="RenamedPipeline"):
        super().__init__(steps, memory=memory, verbose=verbose)
        self.class_name = class_name
        #print(f"Pipeline initialized with class name: {self.class_name}")

    def __repr__(self):
        self.__class__.__name__ = self.class_name
        return ""        

def rename_estimator(estimator, new_class_name):
    # Create a new dynamic class with the desired name
    NewClass = type(new_class_name, (estimator.__class__,), {})
    # Set the estimator's class to this new class
    estimator.__class__ = NewClass
    return estimator

def map_layer_desc_to_sklearn(name, desc):
        match = re.match(r'^(\w+)\((.*)\)$', desc)
        #print(f"Processing description: {desc}")
        #print(f"Match result: {match}")
        if match:
            # If the description matches a function call pattern, extract the class name
            class_name, desc = match.groups()
        estimator = rename_estimator(PlaceholderTransformer(desc=desc), class_name)     
        return (name, estimator)

def nested_dict_to_pipeline(nested_dict, prefix='', pipeline_name=''):
    steps = []
    for key, value in nested_dict.items():
        # print (f'Prefix: {prefix}')
        # print(f"Processing key: {key}, value: {value}")
        if key == '_desc' and isinstance(value, str):
            continue
        # layer_name = f"{prefix}.{key}" if prefix else key
        layer_name = key
        if isinstance(value, dict):
            if '_desc' in value and any(k != '_desc' for k in value):
                # Nested block
                #print(f"Nested block found for layer: {layer_name}")
                if '_desc' in value:
                    inner_pipeline_name = value['_desc']
                    #print(f"Setting pipeline name to: {pipeline_name}")
                sub_pipeline = nested_dict_to_pipeline(value, prefix=layer_name, pipeline_name=inner_pipeline_name[:-1])
                steps.append((layer_name, sub_pipeline))
            else:
                # print(f"Mapping layer description for: {layer_name}")
                steps.append(map_layer_desc_to_sklearn(layer_name, value['_desc']))
        else:
            steps.append(map_layer_desc_to_sklearn(layer_name, value))
    pipeline = Pipeline(steps)
    # Rename the pipeline class to match the first layer's description
    if pipeline_name != '':
        pipeline = rename_estimator(pipeline, pipeline_name)
    return pipeline


def convert_booster_to_lgbmclassifier(booster):
    params = booster.params.copy()
    clf = LGBMClassifier(**params)
    clf.fitted_= True
    return clf


class NeuralNetwork(Pipeline):
    def __init__(self, steps, memory=None, verbose=False, hyperparams=None):
        super().__init__(steps, memory=memory, verbose=verbose)
        self.hyperparams = hyperparams
    def __repr__(self):
        if self.hyperparams:
            return f"NeuralNetwork({self.hyperparams})"

def get_neural_network_estimator_from_autogluon_model(model):
    """
    Extracts a neural network estimator from an AutoGluon model.
    This is a workaround since AutoGluon does not expose the model architecture directly.
    """
    if isinstance(model.model, torch.nn.Module):
        # If the model is a PyTorch neural network, we can extract its architecture
        # This is a workaround since AutoGluon does not expose the model architecture directly.
        nn = str(model.model)
    else:
        # If the model is not a PyTorch neural network, we assume it's a
        # FastAI neural network.
        nn = str(model.model.model)
    
    nested_dict = extract_layers_as_nested_dict(nn)

    # 2. Build sklearn pipeline
    sklearn_pipeline = nested_dict_to_pipeline(nested_dict)

    # 3. Wrap in custom pipeline 
    wrapper = NeuralNetwork(steps=sklearn_pipeline.steps, hyperparams=model.get_params())

    return wrapper

def autogluon_stack_to_sklearn_voting_classifier(model, name="WeightedEnsemble_L2"):
    '''
    Converts an AutoGluon stacked model to a sklearn. Only for HTML diagram creation.
    The function extracts the base models from the AutoGluon stacked model
    and wraps them in a sklearn Pipeline or VotingClassifier that can be used for visualization.
    Args:
        model (TabularPredictor): The AutoGluon model to convert.
        name (str): The name of the model to extract. Default is "WeightedEnsemble_L2".
    Returns:
        sklearn.pipeline.Pipeline or sklearn.ensemble.VotingClassifier: A sklearn-compatible model.
    '''
    predictor = model #TabularPredictor.load(model_path)
    trainer = predictor._trainer

    model = trainer.load_model(name)
    if hasattr(model, 'base_model_names'):
        base_model_names = model.base_model_names
    else:
        base_model_names = [name]
    X_train, y_train = predictor.load_data_internal()
    # train_data, _ = predictor.load_data_internal()
    # X_train = train_data.drop(columns=[predictor.label])
    # y_train = train_data[predictor.label]

    estimators = []

    for model_name in base_model_names:
        model = trainer.load_model(model_name)
        estimator = model.model

        # Case 1: Sklearn-compatible model (RandomForest, ExtraTrees, etc.)
        if isinstance(estimator, BaseEstimator):
            estimators.append((model_name, estimator))

        # Case 2: LightGBM Booster
        elif isinstance(estimator, basic.Booster): 
            try:
                
                booster = estimator#.booster_
                clf = convert_booster_to_lgbmclassifier(booster)
                estimators.append((model_name, clf))
            except Exception as e:
                warnings.warn(f"Failed to convert LightGBM model '{model_name}': {e}")

        # Case 3: AutoGluon Neural Net or other non-sklearn model
        else:
            try:
                if model_name.find("CatBoost") != -1:
                    clf = rename_estimator(PlaceholderTransformer(desc=str(model.get_params())), model_name)
                else:
                    clf = get_neural_network_estimator_from_autogluon_model(model)
                estimators.append((model_name, clf))
            except Exception as e:
                warnings.warn(f"Skipping model '{model_name}': cannot wrap ({e})")

    if not estimators:
        return 
        # raise ValueError("No compatible models found.")
    elif len(estimators) == 1:
        warnings.warn("Only one model found, returning it directly without VotingClassifier.")
        return estimators[0][1]

    return VotingClassifier(estimators=estimators, voting='soft')

class AutogluonModelMlflowWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, model):
        self.model = model

    def predict(self, context, model_input):
        # Convert input DataFrame to the format expected by the AutoGluon model
        return self.model.predict(model_input)
    

    def tabular_to_window(x,y,window_size,group_by=None):
        '''
        Transform tabular data to windowed data in sliding window form with window size as a parameter.
        x: features
        y: target
        window_size: size of the window in number of observations
        group_by: if not None, the data will be grouped by this column before applying the sliding window
        Returns:
        x: transformed features in sliding window form
        y: transformed target in sliding window form
        '''
        x = np.array(x)
        y = np.array(y)
        if window_size == 1:
            return x, y
        features = []
        labels = []
        if group_by is not None:
            unique_groups = np.unique(x[group_by])
            for group in unique_groups:
                group_indices = np.where(x[group_by] == group)[0]
                group_x = x[group_indices]
                group_y = y[group_indices]
                for i in range(0, len(group_x)):
                    if i < window_size:
                        # If we are at the beginning of the group, pad with zeros
                        sample = np.array(group_x[:i]).flatten()
                        sample = np.concatenate((np.zeros(window_size-len(sample)), sample))
                    else:
                        # Normal sliding window
                        sample = np.array(group_x[i-window_size:i]).flatten()
                    features.append(sample)
                    labels.append(group_y[i])
        else:
            # No grouping, apply sliding window directly
            for i in range(0,len(x)): # Revise to generate sliding window with padding
                    if i < window_size:
                        # If we are at the beginning of the group, pad with zeros
                        sample = np.array(group_x[:i]).flatten()
                        sample = np.concatenate((np.zeros(window_size-len(sample)), sample))
                    else:
                        # Normal sliding window
                        sample = np.array(group_x[i-window_size:i]).flatten()
                    features.append(sample)
                    labels.append(y[i])
        return np.array(features), np.array(labels)
    
class ValidationError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
        self.message = message