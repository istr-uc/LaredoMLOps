from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC, SVR
import torch
import src.utils.nn_models.SimpleMultiLayerPerceptron as smlp
import src.utils.nn_models.RNN as rnn
import skorch
from src.utils.model_parameters_dataclasses import (
    RandomForestClassifierParams,
    DecisionTreeClassifierParams,
    SupportVectorClassifierParams,
    KNeighborsClassifierParams,
    MultiLayerPerceptronClassifierParams,
    RNNClassifierParams,
    RandomForestRegressorParams,
    DecisionTreeRegressorParams,
    SupportVectorRegressorParams,
    KNeighborsRegressorParams,
    MultiLayerPerceptronRegressorParams,
    RNNRegressorParams
)

class ModelStrategy:
    def create_model(self, parameters):
        pass

class RandomForestClassifierSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = RandomForestClassifierParams(**parameters)
        return RandomForestClassifier(**params.model_dump())

class DecisionTreeClassifierSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = DecisionTreeClassifierParams(**parameters)
        return DecisionTreeClassifier(**params.model_dump())
    
class SupportVectorMachineClassifierSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = SupportVectorClassifierParams(**parameters)
        return SVC(**params.model_dump())

class KNeighborsClassifierSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = KNeighborsClassifierParams(**parameters)
        return KNeighborsClassifier(**params.model_dump())
    
class RandomForestRegressorSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = RandomForestRegressorParams(**parameters)
        return RandomForestRegressor(**params.model_dump())

class DecisionTreeRegressorSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = DecisionTreeRegressorParams(**parameters)
        return DecisionTreeRegressor(**params.model_dump())

class SupportVectorRegressionSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = SupportVectorRegressorParams(**parameters)
        return SVR(**params.model_dump())

class KNeighborsRegressorSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = KNeighborsRegressorParams(**parameters)
        return KNeighborsRegressor(**params.model_dump())

class SimpleNeuralNetworkReggressorTorchStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = MultiLayerPerceptronRegressorParams(**parameters)
        model_parameters = params.model_dump()
        num_layers = model_parameters.pop('num_layers', 2)
        hidden_size = model_parameters.pop('hidden_size', 64)
        parameters['hidden_sizes'] = [hidden_size] * num_layers
        model = smlp.SimpleMultiLayerPerceptronRegressor(**parameters)
        model = skorch.NeuralNetRegressor(
            module=model,
            max_epochs=parameters.get('max_epochs', 20),
            lr=parameters.get('lr', 0.01),
            iterator_train__shuffle=True,
        )
        return model
    
class SimpleNeuralNetworkClassifierTorchStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = MultiLayerPerceptronClassifierParams(**parameters)
        model_parameters = params.model_dump()
        # Create the base MLP model
        num_layers = int(model_parameters.pop('num_layers', 2))
        hidden_size = int(model_parameters.pop('hidden_size', 64))
        parameters['hidden_sizes'] = [hidden_size] * num_layers
        print(parameters)
        model = smlp.SimpleMultiLayerPerceptronClassifier(**parameters)
        # Wrap the model with skorch's NeuralNetClassifier for easier training
        model = skorch.NeuralNetClassifier(
            module=model,
            max_epochs=parameters.get('max_epochs', 10),
            lr=parameters.get('lr', 0.01),
            iterator_train__shuffle=True,
        )
        return model

class RNNRegressorTorchStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = RNNRegressorParams(**parameters)
        model_parameters = params.model_dump()
        num_layers = int(model_parameters.get('num_layers', 2))
        hidden_size = int(model_parameters.get('hidden_size', 64))
        parameters['hidden_sizes'] = [hidden_size] * num_layers
        model = rnn.RNNRegressor(**parameters)
        model = skorch.NeuralNetRegressor(
            module=model,
            max_epochs=parameters.get('max_epochs', 20),
            lr=parameters.get('lr', 0.01),
            iterator_train__shuffle=True,
        )
        return model

class RNNClassifierTorchStrategy(ModelStrategy):
    def create_model(self, parameters):
        # Validate and parse parameters using Pydantic
        params = RNNClassifierParams(**parameters)
        model_parameters = params.model_dump()
        num_layers = int(model_parameters.get('num_layers', 2))
        hidden_size = int(model_parameters.get('hidden_size', 64))
        parameters['hidden_sizes'] = [hidden_size] * num_layers
        model = rnn.RNNClassifier(**parameters)
        model = skorch.NeuralNetClassifier(
            module=model,
            max_epochs=parameters.get('max_epochs', 20),
            lr=parameters.get('lr', 0.01),
            iterator_train__shuffle=True,
        )
        return model