import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class MyBinaryEncoder(BaseEstimator, TransformerMixin):
    """ Transforms any columns into columns with binary values, showing existence or presence of the feature. Works only on specific columns, as the encoding is hard-coded as shown below (NAs are replaced by 0): 
    
    Alley: 1 if not null, 0 otherwise
    BldgType: 1 if not 1Fam, 0 otherwise
    MiscFeature: 1 if not null, 0 otherwise
    Fence: 1 if not null, 0 otherwise
    MasVnrtype: 0 if None or null, 1 otherwise
    
    Args:
        columns (List): list of column names to transform
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame.
    
    """
    
    _method = {
        'Alley': ['not_null', 'hasAlley'],
        'BldgType': ['not_frequent', '1Fam', 'is1Fam'],
        'MiscFeature': ['not_null', 'hasFeature'],
        'Fence': ['not_null', 'hasFence'],
        'MasVnrType': ['in', ['BrkCmn','BrkFace','CBlock','Stone'], 'hasMasVnr']
    }
    
    def __init__(self, columns):
        self.columns = columns
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        try:
            
            for col in self.columns:
                
                if self._method[col][0] == 'not_null':
                    X.loc[:, col] = X.loc[:, col].notnull().astype(int)
                    X = X.rename(columns={col:self._method[col][1]})
                    
                elif self._method[col][0] == 'not_frequent':
                    X.loc[:, col] = (X.loc[:, col] != self._method.get(col)[1]).astype(int)
                    X = X.rename(columns={col:self._method[col][2]})
                    
                elif self._method[col][0] == 'in':
                    X.loc[:, col] = (X.loc[:, col].isin(self._method.get(col)[1])).astype(int)
                    X = X.rename(columns={col:self._method[col][2]})
                    
            return X
            
        except KeyError:
            cols_error = list(set(self.columns) - set(X.columns))
            raise KeyError('The DataFrame does not include the columns:' % cols_error)