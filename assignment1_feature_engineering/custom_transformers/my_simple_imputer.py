import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MySimpleImputer(BaseEstimator, TransformerMixin):
    """Simple missing value imputer for columns: Lot Frontage, GarageType, GarageYrBlt
    
    Here are the imputations:
    Lot Frontage: 0, indicating no lot frontage
    GarageType: 'None', indicating no garage
    GarageYrBlt: 2100, indicating no garage
        
    Args: 
        columns (List): list of column names to transform
    Returns: 
        pd.DataFrame: transformed pandas DataFrame.
    """
    
    _impute_values = {
        'LotFrontage': 0,
        'GarageType': 'None',
        'GarageYrBlt': 2100
    }
    
    def __init__(self, columns):
        self.columns = columns
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        try:
            
            for col in self.columns:
                X.loc[:, col] = X.loc[:, col].fillna(self._impute_values.get(col))
                    
            return X
            
        except KeyError:
            cols_error = list(set(self.columns) - set(X.columns))
            raise KeyError('The DataFrame does not include the columns:' % cols_error)
        
        
        