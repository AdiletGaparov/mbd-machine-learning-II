import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MyFeatureSelector(BaseEstimator, TransformerMixin):
    """ Selects final columns and returns transformed DataFrame
    
    Args:
        columns (List): list of column names to drop
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame.
        
    """ 
    
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        assert isinstance(X, pd.DataFrame)

        try:
            return X.loc[:, self.columns]
        
        except KeyError:
            cols_error = list(set(self.columns) - set(X.columns))
            raise KeyError("[FeatureSelector] DataFrame does not include the columns:", cols_error)
            
            