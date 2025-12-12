from src.utils.utils import *
from src.utils.preprocessing_strategy import *
from src.utils.model_strategies import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.base import estimator_html_repr, clone
from sklearn.metrics import f1_score, mean_squared_error, recall_score, silhouette_score, r2_score, accuracy_score
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor
import mlflow

class ModelCreation():
    required_parameters = []

    def __init__(self, **kwargs):
        self.validate(kwargs)
        self.set_params_as_attributes(kwargs)

    def validate(self, kwargs):
        missing_params = [param for param in self.required_parameters if param not in kwargs]

        if missing_params:
            raise ValidationError(message=f'Missing parameters. Parameters missing: {missing_params}', status_code=400)
        
    def set_params_as_attributes(self, kwargs):
        for param in kwargs.keys():
            setattr(self, param, kwargs[param])

    def create(self):
        pass

    def get_metrics(self, problem_type, x_test, y_test, predictions):
        metrics = {}
        if problem_type == "classifier":
            accuracy = accuracy_score(y_test, predictions)
            tpr = recall_score(y_test, predictions, average='macro')
            fpr = 1 - recall_score(y_test, predictions, average='macro')
            f1 = f1_score(y_test, predictions, average='macro')
            metrics['accuracy'] = accuracy
            metrics['tpr'] = tpr
            metrics['fpr'] = fpr
            metrics['f1_score'] = f1
        elif problem_type == "cluster":
            silhouette_score_value = silhouette_score(x_test, predictions)
            metrics['silhouette_score'] = silhouette_score_value
        elif problem_type == "regressor":
            mse = mean_squared_error(y_test, predictions)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, predictions)
            metrics['mean_squared_error'] = mse
            metrics['root_mean_squared_error'] = rmse
            metrics['r2_score'] = r2
            
        return metrics

class ModelBasicCreation(ModelCreation):
    required_params = [
        'modelName', 'problemType', 'datasetJSON', 'columnsDataType',
        'target', 'preset', 'evalMetric', 'timeLimit'
    ]

    def create(self):

        dataset = pd.DataFrame.from_dict(self.datasetJSON)
        dataset = dataset.astype(self.columnsDataType)

        
        x = dataset.drop(columns=[self.target])
        y = dataset[self.target]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2) 

        predictor = TabularPredictor(
            label=self.target,
            problem_type=self.problemType,
            eval_metric=self.evalMetric,
        )

        with mlflow.start_run():

            x_train_mlflow = mlflow.data.from_pandas(x_train)
            x_test_mlflow = mlflow.data.from_pandas(x_test)

            mlflow.log_input(x_train_mlflow, context="train")
            mlflow.log_input(x_test_mlflow, context="test")
            
            model = predictor.fit(
                train_data=TabularDataset(x.join(y)),
                presets=self.preset,
                time_limit=self.timeLimit
            )
            algorithm = model._trainer.model_best
            parameters_value = model._trainer.load_model(algorithm).get_params()
            predictions = model.predict(x_test)
            mlflow.log_param("preset", self.preset)
            mlflow.log_param("algorithm", algorithm)
            mlflow.log_params(parameters_value)
            metrics = self.get_metrics(self.problemType, x_test, y_test, predictions)
            mlflow.log_metrics(metrics)
            mlflow.pyfunc.log_model(python_model=AutogluonModelMlflowWrapper(model), artifact_path="model", registered_model_name=self.modelName)
            pipeline = autogluon_stack_to_sklearn_voting_classifier(model)
            mlflow.log_text(estimator_html_repr(pipeline), "estimator.html")
        
        return metrics


    def get_metrics(self, problem_type, x_test, y_test, predictions):
        metrics = {}
        if problem_type == "binary" or problem_type == 'multiclass':
            accuracy = accuracy_score(y_test, predictions)
            tpr = recall_score(y_test, predictions, average='macro')
            fpr = 1 - recall_score(y_test, predictions, average='macro')
            f1 = f1_score(y_test, predictions, average='macro')
            metrics['accuracy'] = accuracy
            metrics['tpr'] = tpr
            metrics['fpr'] = fpr
            metrics['f1_score'] = f1
        elif problem_type == "cluster":
            silhouette_score_value = silhouette_score(x_test, predictions)
            metrics['silhouette_score'] = silhouette_score_value
        elif problem_type == "regressor":
            mse = mean_squared_error(y_test, predictions)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, predictions)
            metrics['mean_squared_error'] = mse
            metrics['root_mean_squared_error'] = rmse
            metrics['r2_score'] = r2
            
        return metrics



class ModelAdvancedCreation(ModelCreation):
    required_params = [
        'modelName', 'problemType', 'datasetJSON', 'columnsDataType',
        'target', 'strategy', 'algorithm', 'implementation'
    ]
    dimensionality_reduction_methods = ['pca', 'selectkbest']

    # def __input_size_and_num_classes(self, x, y, dim_reduction_method=None, dim_reduction_params={},is_time_series=False, time_series_seq_length=1, cols_to_drop=[]):
    #     # input_size = x.shape[1] - len(cols_to_drop)
    #     # if dim_reduction_method is not None:
    #     #     # Compute the input size after dimensionality reduction
    #     #     if dim_reduction_method == 'pca':
    #     #         input_size = dim_reduction_params.get('n_components')
    #     #     elif dim_reduction_method == 'selectkbest':
    #     #         input_size = dim_reduction_params.get('k')
    #     # if is_time_series:
    #     #     # For time series data, the input size is features * seq_length
    #     #     input_size = input_size * time_series_seq_length
    #     if self.problemType == 'classifier':
    #         num_classes = len(y.unique())
    #         return input_size, num_classes
    #     return input_size, None
    
    def __num_classes(self, y):
        num_classes = None
        if self.problemType == 'classifier':
            num_classes = len(y.unique())
        return  num_classes
    
    def create(self):

        preprocessing_methods = self.preprocessingMethods
        parameters_value = self.parametersValue

        dataset = pd.DataFrame.from_dict(self.datasetJSON)
        dataset = dataset.astype(self.columnsDataType)
        is_time_series = False
        if dataset[self.target].dtype == "object":
            label_encoder = LabelEncoder()
            dataset[self.target] = label_encoder.fit_transform(dataset[self.target])


        steps = []
        cols_to_drop = []
        dimensionality_reduction_method = None
        dimensionality_reduction_params = None
        for method, method_data in preprocessing_methods.items():
            # Check for dimensionality reduction methods to handle input size calculation later
            if method in self.dimensionality_reduction_methods:
                dimensionality_reduction_method = method
                dimensionality_reduction_params = method_data.get('params', {})
            # Check for time series methods for later processing of sliding window
            if method == 'time_series_sliding_window':
                is_time_series = True
                time_series_method_data = method_data
                time_series_method = method
                continue
            if method == 'drop':
                cols_to_drop = method_data.get('params', {}).get('columns', [])
            strategy_name = preprocessing_methods[method]['strategy']
            strategy_class = globals().get(strategy_name) 
            if strategy_class != None:
                if 'params' in method_data:
                    step = strategy_class().get_step(method_data['params'])
                else:
                    step = strategy_class().get_step({})            
                steps.append(step)
            else:
                raise ValidationError(message=f"Invalid strategy {strategy_name}", status_code=409)
            
    
        # TODO: Window transformation for time series data (it should always be the last step before the model)
        # Check if the user has specified sliding window transformation for time series data
        if is_time_series:
            time_series_group_column = time_series_method_data['params'].get('timeSeriesGroupColumn')
            time_series_time_column = time_series_method_data['params'].get('timeSeriesTimeColumn', None) # Optional
            seq_length = time_series_method_data['params'].get('seq_length', 1)
            # Order the data group column and time column so that the sliding window is applied correctly
            dataset = dataset.sort_values(by=[time_series_group_column, time_series_time_column])
            # Create transformer for sliding window
            strategy_name = preprocessing_methods[time_series_method]['strategy']
            strategy_class = globals().get(strategy_name) 
            if strategy_class != None:
                if 'params' in time_series_method_data:
                    step = strategy_class().get_step(time_series_method_data['params'])
            # Add the transformer to the pipeline steps
                steps.append(step)
        # Split the data into training and testing sets
        
        x = dataset.drop(columns=[self.target])
        y = dataset[self.target]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle= (not is_time_series))

        strategy_class = globals().get(self.strategy)
        if strategy_class is None:
            raise ValidationError(message="Invalid strategy", status_code=409)
        
        with mlflow.start_run():

            x_train_mlflow = mlflow.data.from_pandas(x_train)
            x_test_mlflow = mlflow.data.from_pandas(x_test)

            mlflow.log_input(x_train_mlflow, context="train")
            mlflow.log_input(x_test_mlflow, context="test")
            
            # For pytorch models, we might need to provide input size and num of classes
            if self.implementation == 'pytorch':
                # Add and fit a pipeline with a sample to determine input size after preprocessing steps
                # Clone the steps to avoid modifying the original steps list
                preprocession_pipeline = clone(Pipeline(steps))
                sample = preprocession_pipeline.fit_transform(x_train.iloc[0:2], y_train.iloc[0:2])
                # input_size, num_classes = self.__input_size_and_num_classes(
                #     x_train,
                #     y_train,
                #     dim_reduction_method=dimensionality_reduction_method,
                #     dim_reduction_params=dimensionality_reduction_params,
                #     is_time_series=is_time_series,
                #     time_series_seq_length= (seq_length if is_time_series else 1),
                #     cols_to_drop=cols_to_drop
                # )
                input_size = sample.shape[1]
                num_classes = self.__num_classes(y_train)
                parameters_value['input_size'] = input_size
                if num_classes is not None:
                    parameters_value['output_size'] = num_classes
                if is_time_series:
                    parameters_value['seq_length'] = seq_length
                # Convert x_train and x_test to float32 for pytorch models

            model = strategy_class().create_model(parameters_value)

            print(parameters_value)
            steps.append(("model", model))
            pipeline = Pipeline(steps)   

            pipeline.fit(x_train, y_train)
            predictions = pipeline.predict(x_test)

            mlflow.log_param("algorithm", self.algorithm)
            mlflow.log_params(parameters_value)
            metrics = self.get_metrics(self.problemType, x_test, y_test, predictions)
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(sk_model=model, artifact_path="model", registered_model_name=self.modelName)
            printable_pipeline = get_printable_pytorch_pipeline(pipeline) if (self.implementation == 'pytorch') else pipeline
            mlflow.log_text(estimator_html_repr(printable_pipeline), "estimator.html")
            
        return metrics