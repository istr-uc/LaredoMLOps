from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC, SVR
import torch
import src.utils.nn_models.SimpleMultiLayerPerceptron as smlp
import src.utils.nn_models.RNN as rnn
import skorch

class ModelStrategy:
    def create_model(self, parameters):
        pass

class RandomForestClassifierSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        return RandomForestClassifier(**parameters)

class DecisionTreeClassifierSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        return DecisionTreeClassifier(**parameters)
    
class SupportVectorMachineClassifierSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        return SVC(**parameters)

class KNeighborsClassifierSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        return KNeighborsClassifier(**parameters)
    
class RandomForestRegressorSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        return RandomForestRegressor(**parameters)

class DecisionTreeRegressorSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        return DecisionTreeRegressor(**parameters)
    
class SupportVectorRegressionSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        return SVR(**parameters)

class KNeighborsRegressorSklearnStrategy(ModelStrategy):
    def create_model(self, parameters):
        return KNeighborsRegressor(**parameters)

class SimpleNeuralNetworkReggressorTorchStrategy(ModelStrategy):
    def create_model(self, parameters):
        num_layers = parameters.get('num_layers', 2)
        hidden_size = parameters.get('hidden_size', 64)
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
        # Create the base MLP model
        num_layers = parameters.pop('num_layers', 2)
        hidden_size = parameters.pop('hidden_size', 64)
        parameters['hidden_sizes'] = [hidden_size] * num_layers
        model = smlp.SimpleMultiLayerPerceptronClassifier(**parameters)
        # Wrap the model with skorch's NeuralNetClassifier for easier training
        model = skorch.NeuralNetClassifier(
            module=model,
            max_epochs=parameters.get('max_epochs', 1),
            lr=parameters.get('lr', 0.01),
            iterator_train__shuffle=True,
        )
        return model

class RNNRegressorTorchStrategy(ModelStrategy):
    def create_model(self, parameters):
        num_layers = parameters.get('num_layers', 2)
        hidden_size = parameters.get('hidden_size', 64)
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
        num_layers = parameters.get('num_layers', 2)
        hidden_size = parameters.get('hidden_size', 64)
        parameters['hidden_sizes'] = [hidden_size] * num_layers
        model = rnn.RNNClassifier(**parameters)
        model = skorch.NeuralNetClassifier(
            module=model,
            max_epochs=parameters.get('max_epochs', 20),
            lr=parameters.get('lr', 0.01),
            iterator_train__shuffle=True,
        )
        return model