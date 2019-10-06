import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class MyLog1pTransformer(BaseEstimator, TransformerMixin):
    """ Apply np.log1p on columns and save it as separate column
    
    Args:
        columns (List): list of column names to transform if given, else all columns
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame.
    
    """
    
    def __init__(self, columns=None):
        self.columns = columns
        
    def fit(self, X, y=None):
        if self.columns:
            self.skewed_cols = self.columns
        else:
            self.skewed_cols = X.skew(axis=0)[X.skew(axis=0)>0.75].index
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        try:
            
            for col in self.skewed_cols:
                X.loc[:, '_'.join([col, 'log'])] = np.log1p(X.loc[:, col])
        
                
            return X
            
        except KeyError:
            cols_error = list(set(self.skewed_cols) - set(X.columns))
            raise KeyError('[LogTransf] DataFrame does not include the columns:', cols_error)