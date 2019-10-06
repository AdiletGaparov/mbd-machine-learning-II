import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class MyLog1pTransformer(BaseEstimator, TransformerMixin):
    """ Apply np.log1p on columns and save it as separate column
    
    Args:
        columns (List): list of column names to transform
        
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
            
            for col in self.columns:
                
                X.loc[:, '_'.join([col, 'log'])] = np.log1p(X.loc[:, col])
                    
            return X
            
        except KeyError:
            cols_error = list(set(self.columns) - set(X.columns))
            raise KeyError('The DataFrame does not include the columns:' % cols_error)