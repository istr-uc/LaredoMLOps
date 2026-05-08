from pydantic import BaseModel
from typing import Optional

class RandomForestClassifierParams(BaseModel):
    n_estimators: Optional[int] = 100
    criterion: Optional[str] = 'gini'
    max_depth: Optional[int] = None
    random_state: Optional[int] = 42
    min_samples_split: Optional[int] = 2
    min_samples_leaf: Optional[int] = 1
    min_weight_fraction_leaf: Optional[float] = 0.0
    max_features: Optional[str] = 'sqrt'
    max_leaf_nodes: Optional[int] = None
    min_impurity_decrease: Optional[float] = 0.0
    class_weight: Optional[str] = 'balanced'
    ccp_alpha: Optional[float] = 0.0
    bootstrap: Optional[bool] = True
    n_jobs: Optional[int] = -1
    verbose: Optional[int] = 0
    warm_start: Optional[bool] = False
    max_samples: Optional[int] = None

class DecisionTreeClassifierParams(BaseModel):
    criterion: Optional[str] = 'gini'
    splitter: Optional[str] = 'best'
    max_depth: Optional[int] = None
    min_samples_split: Optional[int] = 2
    min_samples_leaf: Optional[int] = 1
    min_weight_fraction_leaf: Optional[float] = 0.0
    max_features: Optional[str] = None
    random_state: Optional[int] = 42
    max_leaf_nodes: Optional[int] = None
    min_impurity_decrease: Optional[float] = 0.0
    class_weight: Optional[str] = 'balanced'
    ccp_alpha: Optional[float] = 0.0

class SupportVectorClassifierParams(BaseModel):
    C: Optional[float] = 1.0
    kernel: Optional[str] = 'rbf'
    degree: Optional[int] = 3
    gamma: Optional[str] = 'scale'
    coef0: Optional[float] = 0.0
    shrinking: Optional[bool] = True
    probability: Optional[bool] = False
    tol: Optional[float] = 1e-3
    cache_size: Optional[int] = 200
    class_weight: Optional[str] = None
    verbose: Optional[bool] = False
    max_iter: Optional[int] = -1
    decision_function_shape: Optional[str] = 'ovr'
    break_ties: Optional[bool] = False

class KNeighborsClassifierParams(BaseModel):
    n_neighbors: Optional[int] = 5

class MultiLayerPerceptronClassifierParams(BaseModel):
    num_layers: Optional[int] = 3
    hidden_size: Optional[int] = 64

class RNNClassifierParams(BaseModel):
    num_layers: Optional[int] = 3
    hidden_size: Optional[int] = 64
    sequence_length: Optional[int] = 5

# Regressors

class RandomForestRegressorParams(BaseModel):
    n_estimators: Optional[int] = 100
    criterion: Optional[str] = 'squared_error'
    max_depth: Optional[int] = None
    random_state: Optional[int] = 42
    min_samples_split: Optional[int] = 2
    min_samples_leaf: Optional[int] = 1
    min_weight_fraction_leaf: Optional[float] = 0.0
    max_features: Optional[str] = 'sqrt'
    max_leaf_nodes: Optional[int] = None
    min_impurity_decrease: Optional[float] = 0.0
    ccp_alpha: Optional[float] = 0.0
    bootstrap: Optional[bool] = True
    n_jobs: Optional[int] = -1
    verbose: Optional[int] = 0
    warm_start: Optional[bool] = False
    max_samples: Optional[int] = None
    obb_score: Optional[bool] = False

class DecisionTreeRegressorParams(BaseModel):
    criterion: Optional[str] = 'squared_error'
    splitter: Optional[str] = 'best'
    max_depth: Optional[int] = None
    min_samples_split: Optional[int] = 2
    min_samples_leaf: Optional[int] = 1
    min_weight_fraction_leaf: Optional[float] = 0.0
    max_features: Optional[str] = None
    random_state: Optional[int] = 42
    max_leaf_nodes: Optional[int] = None
    min_impurity_decrease: Optional[float] = 0.0
    ccp_alpha: Optional[float] = 0.0

class SupportVectorRegressorParams(BaseModel):
    C: Optional[float] = 1.0
    kernel: Optional[str] = 'rbf'
    degree: Optional[int] = 3
    gamma: Optional[str] = 'scale'
    coef0: Optional[float] = 0.0
    shrinking: Optional[bool] = True
    tol: Optional[float] = 1e-3
    cache_size: Optional[int] = 200
    verbose: Optional[bool] = False
    max_iter: Optional[int] = -1

class KNeighborsRegressorParams(BaseModel):
    n_neighbors: Optional[int] = 3

class MultiLayerPerceptronRegressorParams(BaseModel):
    num_layers: Optional[int] = 3
    hidden_size: Optional[int] = 64

class RNNRegressorParams(BaseModel):
    num_layers: Optional[int] = 3
    hidden_size: Optional[int] = 64
    sequence_length: Optional[int] = 5