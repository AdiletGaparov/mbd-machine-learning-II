import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MyQualityEncoder(BaseEstimator, TransformerMixin):
    """Custom transformer to encode categorical values with quality information into integers. Works on those  columns, whose values are encoded as shown below (NAs are replaced by 0): 
    
    quality_measures = {'Ex': 5, 'Gd': 4, 'TA': 3, 'Fa': 2, 'Po': 1}
    Ex: Excellence
    Gd: Good
    TA: Typical / Average
    Fa: Fair
    Po: Poor
    
    Args:
        columns (List): list of column names to transform
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame.
    """
    
    _quality_measures = {'Ex':5,'Gd':4,'TA':3,'Fa':2,'Po':1}
    
    def __init__(self, columns):
        self.columns=columns
        
    def fit(self, X, y=None):
        return self
    
    def transform(self,X): 
        assert isinstance(X, pd.DataFrame)
        
        try:
            X.loc[:, self.columns] = X.loc[:, self.columns].replace(self._quality_measures)
            
            # replace NAs with 0 since NAs indicate absence of the feature
            X.loc[:, self.columns] = X.loc[:, self.columns].fillna(0) 
            
            return X 
            
        except KeyError:
            cols_error = list(set(self.columns) - set(X.columns))
            raise KeyError('[QualEnc] DataFrame does not include the columns:', cols_error)