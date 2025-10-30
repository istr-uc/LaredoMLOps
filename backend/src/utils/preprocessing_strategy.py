from sklearn.compose import ColumnTransformer
from src.utils.preprocessing_transfomer import *
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, Normalizer, StandardScaler, OneHotEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.impute import SimpleImputer

class PreprocessingStrategy:
    def get_step(self, params):
        pass

class DropStrategy(PreprocessingStrategy):
    def get_step(self, params):
        preprocessor = ColumnTransformer(
            remainder='passthrough',
            transformers=[('drop_col','drop',params['dropColumns'])]
        )
        return ("Preprocessor", preprocessor)

class MinMaxScalerStrategy(PreprocessingStrategy):
    def get_step(self, params):
        scaler = MinMaxScaler(feature_range=(params['min'], params['max']))
        return ("MinMaxScaler", scaler)
    
class TargetEncoderStrategy(PreprocessingStrategy):
    def get_step(self, params):
        return
    
class NormalizerStrategy(PreprocessingStrategy):
    def get_step(self, params):
        normalizer = Normalizer(**params)
        return ("normalizer", normalizer)

class StandardScalerStrategy(PreprocessingStrategy):
    def get_step(self, params):
        scaler = StandardScaler(**params)
        return ("StandardScaler", scaler)

class OneHotEncoderStrategy(PreprocessingStrategy):
    def get_step(self, params):
        encoder = OneHotEncoder(**params)
        return ("OneHotEncoder", encoder)

class SelectKBestStrategy(PreprocessingStrategy):
    def get_step(self, params):
        selector = SelectKBest(**params)
        return ("SelectKBest", selector)

class PCAStrategy(PreprocessingStrategy):
    def get_step(self, params):
        pca = PCA(**params)
        return ("PCA", pca)
    
class SimpleImputerStrategy(PreprocessingStrategy):
    def get_step(self, params):
        imputer = SimpleImputer(**params)
        return ("SimpleImputer", imputer)
    
class FfillStrategy(PreprocessingStrategy):
    def get_step(self, params):
        return ("Ffill", FfillTransformer())

class BfillStrategy(PreprocessingStrategy):
    def get_step(self, params):
        return ("Bfill", BfillTransformer())

class TabularToWindowStrategy(PreprocessingStrategy):
    def get_step(self, params):
        return ("TabularToWindow", TabularToWindowTransformer(**params))