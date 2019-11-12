import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class MyBinaryEncoder(BaseEstimator, TransformerMixin):
    """ Transforms 3 columns with categorical or continuous values into binary 
    
    MiscFeature: 1 if not null, 0 otherwise
    MasVnrType: 1 if MasVnrType is Stone, else 0
    CentralAir: 1 if Y, 0 if N
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame.
    
    """
    
    def __init__(self):
        pass
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        try:
            
            # MiscFeature
            X.loc[:, 'MiscFeature'] = X.loc[:, 'MiscFeature'].notnull().astype(int)
            X = X.rename(columns={'MiscFeature': 'hasMiscFeature'})
            
            # CentralAir
            X.loc[:, 'CentralAir'] = X.loc[:, 'CentralAir'].replace({'Y':1, 'N':0})
            
            # MasVnrType
            X.loc[:, 'MasVnrType'] = (X.loc[:, 'MasVnrType']=='Stone').astype(int)
            X = X.rename(columns={'MasVnrType': 'MasVnrStone'})
                    
            return X
            
        except KeyError:
            cols_error = list(set(['MiscFeature', 'CentralAir', 'MasVnrType']) - set(X.columns))
            raise KeyError('[BinaryEnc] DataFrame does not include the columns:', cols_error)