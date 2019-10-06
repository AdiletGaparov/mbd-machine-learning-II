import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MyRoomsFeatures(BaseEstimator, TransformerMixin):
    """Adds features based on value added:  Size * Quality.
        
    Args: 
        pool (Bool): True (default) to include value feature for Pool, False otherwise
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame with new features
    """
    
    def __init__(self, ):
       
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        try:
            
                    
            return X
            
        except KeyError:
            cols_related = []
            
            cols_error = list(set(cols_related) - set(X.columns))
            raise KeyError('The DataFrame does not include the columns:' % cols_error)
        
        
        