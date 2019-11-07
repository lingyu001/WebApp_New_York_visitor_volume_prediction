

import dill

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn_pandas import DataFrameMapper
from sklearn.ensemble import RandomForestRegressor

def rfr_predict(data):

    rfr_pipe = dill.load(open('static/rfr_pipe.dill', 'rb'))
    
    result = rfr_pipe.predict(data)
    
    return result
