import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MyRoomsFeatures(BaseEstimator, TransformerMixin):
    """Add rooms-based features, taking into account Bathrooms, Bedrooms and space
        
    Args: 
        tot_baths (Bool): True (default) to include feature indicating total number of bathrooms in the property
        baths_vs_bedrooms: True (default) to include feature indicating number of bathrooms per bedroom
        bedrooms_vs_area: True (default) to include feature indicating number of bedrooms per square feet
        bedrooms_vs_rooms: True (default) to include feature indicating share of bedrooms per all rooms
        rooms_vs_area: True (default) to include feature indicating number of rooms per square feet
        
    Returns: 
        pd.DataFrame: transformed pandas DataFrame with new features
    """
    
    def __init__(self, tot_bath=True, bath_vs_bedrooms=True, bedrooms_vs_area=True, bedrooms_vs_rooms=True, rooms_vs_area=True):
        self.tot_bath=tot_bath
        self.bath_vs_bedrooms = bath_vs_bedrooms
        self.bedrooms_vs_area = bedrooms_vs_area
        self.bedrooms_vs_rooms = bedrooms_vs_rooms
        self.rooms_vs_area = rooms_vs_area
       

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
                
        assert isinstance(X, pd.DataFrame)
        
        try:
            
            if self.tot_bath:
                X.loc[:, 'TotBath'] = X.loc[:, 'FullBath'] + 0.5*X.loc[:,'HalfBath'] + X.loc[:,'BsmtFullBath'] + 0.5*X.loc[:,'BsmtHalfBath']
                    
            if self.bath_vs_bedrooms:
                X.loc[X['BedroomAbvGr']==0,'Bath_vs_Bedrooms'] = 0
                total_baths = X.loc[:, 'FullBath'] + 0.5*X.loc[:,'HalfBath'] + X.loc[:,'BsmtFullBath'] + 0.5*X.loc[:,'BsmtHalfBath']
                X.loc[X['BedroomAbvGr']>0, 'Bath_vs_Bedrooms'] = total_baths / X.loc[:, 'BedroomAbvGr']
                
            if self.bedrooms_vs_area:
                X.loc[X['GrLivArea']==0, 'Bedrooms_vs_LivArea'] = 0
                X.loc[X['GrLivArea']>0, 'Bedrooms_vs_LivArea'] = X.loc[:, 'BedroomAbvGr'] / X.loc[:, 'GrLivArea']
            
            if self.bedrooms_vs_rooms:
                X.loc[X['TotRmsAbvGrd']==0, 'Bedrooms_vs_Rooms'] = 0
                X.loc[X['TotRmsAbvGrd']>0, 'Bedrooms_vs_Rooms'] = X.loc[:, 'BedroomAbvGr'] / X.loc[:, 'TotRmsAbvGrd']
                
            if self.rooms_vs_area:
                X.loc[X['GrLivArea']==0, 'Rooms_vs_LivArea'] = 0
                X.loc[X['GrLivArea']>0, 'Rooms_vs_LivArea'] = X.loc[:, 'TotRmsAbvGrd'] / X.loc[:, 'GrLivArea']
                
                
            return X
            
        except KeyError:
            cols_related = ['BedroomAbvGr', 'GrLivArea','TotRmsAbvGrd', 
                           'FullBath','HalfBath','BsmtFullBath','BsmtHalfBath']
            
            cols_error = list(set(cols_related) - set(X.columns))
            raise KeyError('[RoomsFeature] DataFrame does not include the columns:', cols_error)
        
        
        