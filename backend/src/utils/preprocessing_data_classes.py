from pydantic import BaseModel
from typing import Optional

# Define a class for preprocessing data parameters one for each preprocessing method
class DropParams(BaseModel):
    dropColumns: Optional[list[str]]

class MinMaxScalerParams(BaseModel):
    min: Optional[float] = 0.0
    max: Optional[float] = 1.0

class SelectKBestParams(BaseModel):
    k: Optional[int] = 10

class PCAParams(BaseModel):
    n_components: Optional[int] = 2

class SimpleImputerParams(BaseModel):
    strategy: Optional[str] = 'mean'

class FfillParams(BaseModel):
    pass

class TabularToWindowStrategyParams(BaseModel):
    sequence_length: Optional[int] = 5
    time_column: Optional[str] = 'timestamp'
    target_column: Optional[str] = 'target'
    group_by_column: Optional[str] = None
