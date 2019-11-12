import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MyQualityFeatures(BaseEstimator, TransformerMixin):
    """Adds features based on quality / conditions
        
    Args: 
        high_quality_sf (Bool): True (default) to include High Quality SF = (1-LowQualFinSF)/GrLivArea, False otherwise
        overall_mult (Bool): True (default) to include feature equal to a multiplication of OverallQual and OverallCond, False otherwise
        overall_sum (Bool): True (default) to include feature equal to a sum of OverallQual and OverallCond, False otherwise
        external_mult (Bool): True (default) to include feature equal to a multiplication of ExterQual and ExterCond, False otherwise
        external_sum (Bool): True (default) to include feature equal to a sum of ExterQual and ExterCond, False otherwise
        garage_mult (Bool): True (default) to include feature equal to a multiplication of GarageQual and GarageCond, False otherwise
        garage_sum (Bool): True (default) to include feature equal to a sum of GarageQual and GarageCond, False otherwise,
        basement_mult (Bool): True (default) to include feature equal to a multiplication of BsmtQual and BsmtCond, False otherwise
        basement_sum (Bool): True (default) to include feature equal to a sum of BsmtQual and BsmtCond, False otherwise
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame with new features
    """
    
    def __init__(self, high_quality_sf=True, overall_mult=True, overall_sum=True, 
                 external_mult=True, external_sum=True, garage_mult=True, garage_sum=True,
                basement_mult=True, basement_sum=True):
        self.high_quality_sf = high_quality_sf
        self.overall_mult = overall_mult
        self.overall_sum = overall_sum
        self.external_mult = external_mult
        self.external_sum = external_sum
        self.garage_mult = garage_mult
        self.garage_sum = garage_sum
        self.basement_mult = basement_mult
        self.basement_sum = basement_sum
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        try:
            
            if self.high_quality_sf:
                X.loc[X['GrLivArea']==0, 'HighQualSF_percent'] = 0
                X.loc[X['GrLivArea']>0, 'HighQualSF_percent'] = (1-X.loc[:, 'LowQualFinSF']) / X.loc[:, 'GrLivArea']
            
            if self.overall_mult: 
                X.loc[:, 'OverallEval_mult'] = X.loc[:, 'OverallQual'] * X.loc[:, 'OverallCond']
                
            if self.overall_sum:
                X.loc[:, 'OverallEval_sum'] = X.loc[:, 'OverallQual'] + X.loc[:, 'OverallCond']
                
            if self.external_mult:
                X.loc[:, 'ExterEval_mult'] = X.loc[:, 'ExterQual'] * X.loc[:, 'ExterCond']
            
            if self.external_sum:
                X.loc[:, 'ExterEval_sum'] = X.loc[:, 'ExterQual'] + X.loc[:, 'ExterCond']
                
            if self.garage_mult:
                X.loc[:, 'GarageEval_mult'] = X.loc[:, 'GarageQual'] * X.loc[:, 'GarageCond']
                
            if self.garage_sum:
                X.loc[:, 'GarageEval_sum'] = X.loc[:, 'GarageQual'] + X.loc[:, 'GarageCond']
                
            if self.basement_mult:
                X.loc[:, 'BsmtEval_mult'] = X.loc[:, 'BsmtQual'] * X.loc[:, 'BsmtCond']
            
            if self.basement_sum:
                X.loc[:, 'BsmtEval_sum'] = X.loc[:, 'BsmtQual'] + X.loc[:, 'BsmtCond']
                
                    
            return X
            
        except KeyError:
            cols_related = ['LowQualFinSF', 'OverallQual', 'OverallCond',
                            'ExterQual', 'ExterCond', 'GarageQual', 
                            'GarageCond', 'BsmtQual', 'BsmtCond']
            cols_error = list(set(cols_related) - set(X.columns))
            raise KeyError('[QualFeature] DataFrame does not include the columns:', cols_error)
        
        
        