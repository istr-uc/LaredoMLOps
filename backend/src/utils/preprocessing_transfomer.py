import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class FfillTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = pd.DataFrame(X)
        df = df.ffill().bfill()
        X = np.array(df)
        return X

class BfillTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = pd.DataFrame(X)
        df = df.bfill().ffill()
        X = np.array(df)
        return X
    
class TabularToWindowTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, window_size=5, group_by=None):
        self.window_size = window_size
        self.group_by = group_by
    def fit(self, X, y=None):
        return self

    def transform(self,x):
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
        #y = np.array(y)
        if self.window_size == 1:
            return x#, y
        features = []
        # labels = []
        if self.group_by is not None:
            unique_groups = np.unique(x[self.group_by])
            for group in unique_groups:
                group_indices = np.where(x[self.group_by] == group)[0]
                group_x = x[group_indices]
                #group_y = y[group_indices]
                for i in range(0, len(group_x)):
                    if i < self.window_size:
                        # If we are at the beginning of the group, pad with zeros
                        sample = np.array(group_x[:i]).flatten()
                        sample = np.concatenate((np.zeros(self.window_size-len(sample)), sample))
                    else:
                        # Normal sliding window
                        sample = np.array(group_x[i-self.window_size:i]).flatten()
                    features.append(sample)
                    # labels.append(group_y[i])
        else:
            # No grouping, apply sliding window directly
            for i in range(0,len(x)): # Revise to generate sliding window with padding
                    if i < self.window_size:
                        # If we are at the beginning of the group, pad with zeros
                        sample = np.array(group_x[:i]).flatten()
                        sample = np.concatenate((np.zeros(self.window_size-len(sample)), sample))
                    else:
                        # Normal sliding window
                        sample = np.array(group_x[i-self.window_size:i]).flatten()
                    features.append(sample)
                    # labels.append(y[i])
        return np.array(features)#, np.array(labels)