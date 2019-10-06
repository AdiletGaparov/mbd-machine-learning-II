import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MyValueAddedFeatures(BaseEstimator, TransformerMixin):
    """Adds features based on value added:  Size * Quality.
        
    Args: 
        pool (Bool): True (default) to include value feature for Pool, False otherwise
        kitchen (Bool): True (default) to include value feature for Kitchen, False otherwise
        garage (Bool): True (default) to include value feature for Garage, False otherwise
        fireplace (Bool): True (default) to include value feature for Fireplace, False otherwise
        basement (Bool): True (default) to include value feature for Basement, False otherwise
        basement_adv (Bool): True (default) to include advanced value feature for Basement (multiplied by BsmtExposure), False otherwise
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame with new features
    """
    
    def __init__(self, pool=True, kitchen=True, garage=True, fireplace=True, basement=True, basement_adv=True):
        self.pool = pool
        self.kitchen = kitchen
        self.garage = garage
        self.fireplace = fireplace
        self.basement = basement
        self.basement_adv = basement_adv
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        try:
            
            if self.pool:
                X.loc[:, 'PoolValue'] = X.loc[:, 'PoolArea'] * X.loc[:, 'PoolQC']
                
            if self.kitchen:
                X.loc[:, 'KitchenValue'] = X.loc[:, 'KitchenAbvGr'] * X.loc[:, 'KitchenQual']
            
            if self.fireplace: 
                X.loc[:, 'FireplacesValue'] = X.loc[:, 'Fireplaces'] * X.loc[:, 'FireplaceQu']
                
            if self.garage:
                X.loc[:, 'GarageValue'] = X.loc[:, 'GarageArea'] * X.loc[:, 'GarageQual']
                
            if self.basement:
                X.loc[:, 'BsmtValue'] = X.loc[:, 'BsmtFinType1'] * X.loc[:, 'BsmtFinSF1'] + X.loc[:, 'BsmtFinType2'] * X.loc[:, 'BsmtFinSF2']
            
            if self.basement_adv:
                bsmt_value = X.loc[:, 'BsmtFinType1'] * X.loc[:, 'BsmtFinSF1'] + X.loc[:, 'BsmtFinType2'] * X.loc[:, 'BsmtFinSF2']
                X.loc[:, 'BsmtValueAdv'] = bsmt_value * X.loc[:, 'BsmtExposure']
                    
            return X
            
        except KeyError:
            cols_related = ['PoolArea', 'PoolQC', 'Fireplaces', 'FireplaceQu', 
                            'KitchenAbvGr', 'KitchenQual', 'GarageArea','GarageQual', 
                            'BsmtFinType1','BsmtFinSF1','BsmtFinType2','BsmtFinSF2', 
                            'BsmtExposure']
            
            cols_error = list(set(cols_related) - set(X.columns))
            raise KeyError('[ValueFeatures] DataFrame does not include the columns:', cols_error)
        
        
        