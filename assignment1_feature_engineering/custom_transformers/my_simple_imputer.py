import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MySimpleImputer(BaseEstimator, TransformerMixin):
    """Simple missing value imputer for columns: Lot Frontage, GarageType, GarageYrBlt
    
    Here are the imputations:
    Lot Frontage: 0, indicating no lot frontage
    GarageYrBlt: 2100, indicating no garage
    BsmtFinSF1, BsmtFinSF2, BsmtUnfSF, TotalBsmtSF, BsmtFullBath, BsmtHalfBath: 0, indicating no basement
    GarageCars, GarageArea: 0
    
    Returns: 
        pd.DataFrame: transformed pandas DataFrame.
    """
    
    _impute_values = {
        'LotFrontage': 0,
        'GarageYrBlt': 2100,
        'BsmtFinSF1': 0,
        'BsmtFinSF2': 0,
        'BsmtUnfSF': 0,
        'TotalBsmtSF': 0,
        'BsmtFullBath': 0,
        'BsmtHalfBath': 0,
        'GarageCars': 0,
        'GarageArea': 0
    }
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        try:
            
            for col in self._impute_values.keys():
                X.loc[:, col] = X.loc[:, col].fillna(self._impute_values.get(col))
                    
            return X
            
        except KeyError:
            cols_error = list(set(self._impute_values.keys()) - set(X.columns))
            raise KeyError('[Imputer] DataFrame does not include the columns:', cols_error)
        
        
        