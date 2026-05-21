from sklearn.compose import ColumnTransformer
from src.utils.preprocessing_transfomer import *
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, Normalizer, StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.impute import SimpleImputer
from src.utils.preprocessing_data_classes import *

class PreprocessingStrategy:
    def get_step(self, params):
        pass

class DropStrategy(PreprocessingStrategy):
    def get_step(self, params):
        params = DropParams(**params).model_dump()
        preprocessor = ColumnTransformer(
            remainder='passthrough',
            verbose_feature_names_out=False,
            transformers=[('drop_col','drop',params['dropColumns'])]
        )
        return ("Preprocessor", preprocessor)

class MinMaxScalerStrategy(PreprocessingStrategy):
    def get_step(self, params):
        params = MinMaxScalerParams(**params).model_dump()
        scaler = MinMaxScaler(feature_range=(params['min'], params['max']))
        return ("MinMaxScaler", scaler)
    
# class TargetEncoderStrategy(PreprocessingStrategy):
#     def get_step(self, params):
#         return

class OrdinalEncoderStrategy(PreprocessingStrategy):
    def get_step(self, params):
        params = OrdinalEncoderParams(**params).model_dump()
        columns = params.pop('columns')
        encoder = OrdinalEncoder(
            handle_unknown='use_encoded_value',
            unknown_value=-1,
        )
        preprocessor = ColumnTransformer(
            remainder='passthrough',
            verbose_feature_names_out=False,
            transformers=[('ordinal_encoder', encoder, columns)]
        )
        return ("OrdinalEncoder", preprocessor)
    
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
        params = SelectKBestParams(**params).model_dump()
        selector = SelectKBest(**params)
        return ("SelectKBest", selector)

class PCAStrategy(PreprocessingStrategy):
    def get_step(self, params):
        params = PCAParams(**params).model_dump()
        pca = PCA(**params)
        return ("PCA", pca)
    
class SimpleImputerStrategy(PreprocessingStrategy):
    def get_step(self, params):
        params = SimpleImputerParams(**params).model_dump()
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
        params = TabularToWindowStrategyParams(**params).model_dump()
        return ("TabularToWindow", TabularToWindowTransformer(**params))