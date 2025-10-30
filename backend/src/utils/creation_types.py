from src.utils.utils import *
from src.utils.preprocessing_strategy import *
from src.utils.model_strategies import *
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.base import estimator_html_repr
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
        'target', 'strategy', 'algorithm'
    ]

    def create(self):

        preprocessing_methods = self.preprocessingMethods
        parameters_value = self.parametersValue

        dataset = pd.DataFrame.from_dict(self.datasetJSON)
        dataset = dataset.astype(self.columnsDataType)

        if dataset[self.target].dtype == "object":
            label_encoder = LabelEncoder()
            dataset[self.target] = label_encoder.fit_transform(dataset[self.target])


        steps = []

        for method, method_data in preprocessing_methods.items():
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
            
        x = dataset.drop(columns=[self.target])
        y = dataset[self.target]

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

        strategy_class = globals().get(self.strategy)
        if strategy_class is None:
            raise ValidationError(message="Invalid strategy", status_code=409)
        
        with mlflow.start_run():

            x_train_mlflow = mlflow.data.from_pandas(x_train)
            x_test_mlflow = mlflow.data.from_pandas(x_test)

            mlflow.log_input(x_train_mlflow, context="train")
            mlflow.log_input(x_test_mlflow, context="test")


            model = strategy_class().create_model(parameters_value)

            
            steps.append(("model", model))
            pipeline = Pipeline(steps)   

            pipeline.fit(x_train, y_train)
            predictions = pipeline.predict(x_test)

            mlflow.log_param("algorithm", self.algorithm)
            mlflow.log_params(parameters_value)
            metrics = self.get_metrics(self.problemType, x_test, y_test, predictions)
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(sk_model=model, artifact_path="model", registered_model_name=self.modelName)
            mlflow.log_text(estimator_html_repr(pipeline), "estimator.html")
            
        return metrics