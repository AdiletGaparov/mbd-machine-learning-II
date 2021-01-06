import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
            
            
class MyOtherOrdinalEncoder(BaseEstimator, TransformerMixin):
    """ Custom transformer to encode categorical values with ordinal meaning into integers. Works only on specific columns, as the encoding is hard-coded as shown below (NAs are replaced by 0): 
    
    _order_encoder = {
        'BsmtExposure':  {'Gd': 4, 'Av': 3, 'Mn': 2, 'No': 1},
        'BsmtFinType1': {'GLQ': 6, 'ALQ': 5, 'BLQ': 4, 'Rec': 3, 'LwQ': 2, 'Unf': 1},
        'BsmtFinType2': {'GLQ': 6, 'ALQ': 5, 'BLQ': 4, 'Rec': 3, 'LwQ': 2, 'Unf': 1},
        'GarageFinish': {'Fin': 3, 'RFn': 2, 'Unf': 1},
        'LotShape': {'Reg': 4, 'IR1': 3, 'IR2': 2, 'IR3': 1},
        'PavedDrive': {'Y': 1,'P': 0.5, 'N': 0},
        'Electrical': {'SBrkr': 4, 'FuseA': 3, 'FuseF': 2, 'FuseP': 1, 'Mix': 2.5},
        'Functional': {'Typ': 8, 'Min1': 7, 'Min2': 6, 'Mod': 5, 'Maj1': 4,'Maj2': 3,'Sev': 2,'Sal': 1},
        'LandSlope': {'Gtl': 1, 'Mod': 2, 'Sev': 3},
        'HouseStyle': {'1Story': 1, '1.5Fin': 1.5, '1.5Unf': 1.25, '2Story': 2, '2.5Fin': 2.5, '2.5Unf': 2.25, 'SFoyer': 2, 'SLvl': 2}
    }
    
    
    Args:
        columns (List): list of column names to transform
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame.
    """
    
    _order_encoder = {
        'BsmtExposure':  {'Gd': 4, 'Av': 3, 'Mn': 2, 'No': 1},
        'BsmtFinType1': {'GLQ': 6, 'ALQ': 5, 'BLQ': 4, 'Rec': 3, 'LwQ': 2, 'Unf': 1},
        'BsmtFinType2': {'GLQ': 6, 'ALQ': 5, 'BLQ': 4, 'Rec': 3, 'LwQ': 2, 'Unf': 1},
        'GarageFinish': {'Fin': 3, 'RFn': 2, 'Unf': 1},
        'LotShape': {'Reg': 4, 'IR1': 3, 'IR2': 2, 'IR3': 1},
        'PavedDrive': {'Y': 1,'P': 0.5, 'N': 0},
        'Electrical': {'SBrkr': 4, 'FuseA': 3, 'FuseF': 2, 'FuseP': 1, 'Mix': 2.5},
        'Functional': {'Typ': 8, 'Min1': 7, 'Min2': 6, 'Mod': 5, 'Maj1': 4,'Maj2': 3,'Sev': 2,'Sal': 1},
        'LandSlope': {'Gtl': 1, 'Mod': 2, 'Sev': 3},
        'HouseStyle': {'1Story': 1, '1.5Fin': 1.5, '1.5Unf': 1.25, '2Story': 2, '2.5Fin': 2.5, '2.5Unf': 2.25, 'SFoyer': 2, 'SLvl': 2}
    }

    def __init__(self, columns):
        self.columns = columns
    
    def fit(self, X,y=None):
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        try:
            
            for col in self.columns:
                X.loc[:, col] = X.loc[:, col].replace(self._order_encoder.get(col))
            
            # replace NAs with 0 since NAs indicate absence of the feature
            X.loc[:, self.columns] = X.loc[:, self.columns].fillna(0)
                
            return X 
            
        except KeyError:
            cols_error = list(set(self.columns) - set(X.columns))
            raise KeyError('[OrdEnc] DataFrame does not include the columns:', cols_error)
