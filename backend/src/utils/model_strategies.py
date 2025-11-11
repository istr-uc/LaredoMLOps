from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC, SVR

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
