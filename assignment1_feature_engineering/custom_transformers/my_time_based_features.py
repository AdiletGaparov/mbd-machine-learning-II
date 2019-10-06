import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MyTimeBasedFeatures(BaseEstimator, TransformerMixin):
    """Adds features based on time: YrSold, MoSold, YearBuilt, GarageYrBlt, YearRemodAdd
        
    Args: 
        season (Bool): True (default) to include feature for season based on month sold
        since_house_built (Bool): True (default) to include feature for time since house was built (YrSold-YearBuilt)
        since_house_remod (Bool): True (default) to include feature for time since house was remodeled
        since_garage_built (Bool): True (default) to include feature for time since garage was built
        isRemodeled (Bool): True (default) to include feature indicating if house was remodeled
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame with new features
    """
    
    def __init__(self, season=True, since_house_built=True, since_house_remod=True, since_garage_built=True, isRemodeled=True):
        self.season = season
        self.since_house_built = since_house_built
        self.since_house_remod = since_house_remod
        self.since_garage_built = since_garage_built
        self.isRemodeled = isRemodeled
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        assert isinstance(X, pd.DataFrame)
        
        try:
            
            if self.season:
                season_dict = {1:'Winter',2:'Winter', 3: 'Spring':, 4: 'Spring', 
                               5: 'Spring': 6: 'Summer': 7: 'Summer': 8: 'Summer',
                              9: 'Autumn', 10: 'Autumn', 11: 'Autumn', 12: 'Winter'}
                
                X.loc[:, 'season'] = X.loc[:,'MoSold'].replace(season_dict)
                
            if self.since_house_built:
                X.loc[:, 'YrsSinceBuilt'] = X.loc[:, 'YrSold'] - X.loc[:,'YearBuilt'] 
            
            if self.since_house_remod:
                X.loc[:, 'YrsSinceRemod'] = X.loc[:, 'YrSold'] - X.loc[:, 'YearBuilt']
                
            if self.since_garage_built:
                X.loc[:, 'GarageYrsSinceBuilt'] = X.loc[:, 'YrSold'] - X.loc[:, 'GarageYrBlt']
                
            if self.isRemodeled:
                X.loc[:, 'isRemodeled'] = ((X.loc[:, 'YearBuilt'] - X.loc[:, 'YearRemodAdd']) > 0).astype(int)
                    
            return X
            
        except KeyError:
            cols_related = ['YrSold', 'YearBuilt', 'GarageYrBlt', 'YearRemodAdd', 'MoSold']
            cols_error = list(set(cols_related) - set(X.columns))
            raise KeyError('The DataFrame does not include the columns:' % cols_error)
        
        
        