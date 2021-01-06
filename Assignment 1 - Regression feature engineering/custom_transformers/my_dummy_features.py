import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MyDummyFeatures(BaseEstimator, TransformerMixin):
    """Dummification of categorical features
    
    Returns: 
        pd.DataFrame: transformed pandas DataFrame.
    """
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        return pd.get_dummies(X, drop_first=True)
            
        
        
        