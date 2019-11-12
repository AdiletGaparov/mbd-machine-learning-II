import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MySpaceBasedFeatures(BaseEstimator, TransformerMixin):
    """Adds features based on space / area in square feet
    
        
    Args: 
        bsmt_finished (Bool): True (default) to include feature indicating the percentage of Basement finished if exists
        bsmt_vs_living (Bool): True (default) to include feature indicating the ratio of total basement area to above ground living area
        porch (Bool): True (default) to include feature indicating total porch area in sq.feet
        lot_left_percent (Bool): True (default) to include feature indicating percentage of lot space left
        bsmt_vs_lot (Bool): True (default) to include feature indicating ratio of total basement area to total lot area
        
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame with new features
    """
    
    def __init__(self, bsmt_finished_percent=True, bsmt_vs_living=True, porch=True, lot_left_percent=True, bsmt_vs_lot=True):
        self.bsmt_finished_percent=bsmt_finished_percent
        self.bsmt_vs_living = bsmt_vs_living
        self.porch = porch
        self.lot_left_percent = lot_left_percent
        self.bsmt_vs_lot = bsmt_vs_lot
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        try:
            
            if self.bsmt_finished_percent:
                
                X.loc[X['TotalBsmtSF']==0, 'BsmtFinPercent'] = 0
                X.loc[X['TotalBsmtSF']>0, 'BsmtFinPercent'] = (1-X.loc[:, 'BsmtUnfSF']) / X.loc[:, 'TotalBsmtSF']
            
            if self.bsmt_vs_living:
                X.loc[X['GrLivArea']==0, 'Bsmt_vs_LivArea'] = 0
                X.loc[X['GrLivArea']>0, 'Bsmt_vs_LivArea'] = X.loc[:,'TotalBsmtSF'] / X.loc[:,'GrLivArea']
                
            if self.porch:
                X.loc[:,'TotalPorch'] = X.loc[:, 'WoodDeckSF'] +  X.loc[:, 'OpenPorchSF'] + X.loc[:, 'EnclosedPorch'] \
                                        + X.loc[:, '3SsnPorch'] + X.loc[:, 'ScreenPorch']
            
            if self.lot_left_percent:
                total_porch = X.loc[:, 'WoodDeckSF'] +  X.loc[:, 'OpenPorchSF'] + X.loc[:, 'EnclosedPorch'] \
                            + X.loc[:, '3SsnPorch'] + X.loc[:, 'ScreenPorch']
                
                X.loc[X['LotArea']==0, 'LotLeft_percent'] = 0
                X.loc[X['LotArea']>0,'LotLeft_percent'] = (X.loc[:,'LotArea']-X.loc[:, 'TotalBsmtSF'] \
                                              - X.loc[:, 'GarageArea']-X.loc[:, 'PoolArea']-X.loc[:, 'WoodDeckSF']\
                                              -total_porch) / X.loc[:, 'LotArea']
                
            if self.bsmt_vs_lot:
                X.loc[X['LotArea']==0, 'Bsmt_vs_Lot'] = 0
                X.loc[X['LotArea']>0, 'Bsmt_vs_Lot'] = X.loc[:,'TotalBsmtSF'] / X.loc[:, 'LotArea']
                
            return X
            
        except KeyError:
            cols_related = ['BsmtUnfSF', 'TotalBsmtSF','GrLivArea','WoodDeckSF',
                            'OpenPorchSF','EnclosedPorch','3SsnPorch','ScreenPorch',
                           'LotArea','GarageArea','PoolArea']
            
            cols_error = list(set(cols_related) - set(X.columns))
            raise KeyError('[SpaceFeatures] DataFrame does not include the columns:', cols_error)