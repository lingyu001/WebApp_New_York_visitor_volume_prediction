
import pandas as pd
import numpy as np
from shapely.geometry import Point
import requests as rq
import json
from pandas.io.json import json_normalize
import datetime as dt
import geopandas as gpd
import dill

gpd_zip = dill.load(open('static/gpd_zip.dill', 'rb'))

## Functions

def valid_zip(x):
    """
    validate if zipcode within New York analysis area (Manhattan, borrklyn and queens).
    
    Input zipcode
    return 1 if valid, 0 otherwise.
    """
    m_zip = [83,10286,10276,10268,10256,10249,10159,10150,10116,10113,10108,10101,10008,10282,10281,10280,10279,10278,10275,
             10271,10270,10199,10178,10177,10176,10175,10174,10173,10172,10171,10170,10169,10168,10167,10166,10165,
             10162,10161,10158,10155,10154,10153,10152,10151,10128,10123,10122,10121,10120,10119,10118,10115,10112,
             10111,10110,10107,10106,10105,10104,10103,10099,10098,10095,10090,10069,10060,10055,10048,10047,10045,10044,
             10041,10040,10039,10038,10037,10036,10035,10034,10033,10032,10031,10030,10029,10028,10027,10026,10025,
             10024,10023,10022,10021,10020,10019,10018,10017,10016,10015,10014,10013,10012,10011,10010,10009,10007,
             10006,10005,10004,10003,10002,10001,10065,10075,10080,
             10285,10203,10178,10017,10178,10168,10167,10177,# supplementary
             10175,10166,10171,10176,10174,10165,10170,10173,10169,10172,10019, 10105, 10097, 10104, 10107, 10103, 10106,
             10022, 10055, 10155, 10152, 10153, 10151, 10154, 10001, 10120, 10119, 10118, 10123, 10122, 10121,
             10005, 10081, 10286, 10260, 10271, 10259, 10043, 10270, 10265, 10203,10036, 10096, 10196, 10110
            ]
    brooklyn_zip = [11256,11252,11249,11243,11242,11241,11239,11238,11237,11236,11235,11234,11233,11232,11231,
                    11230,11229,11228,11226,11225,11224,11223,11222,11221,11220,11219,11218,11217,11216,11215,
                    11214,11213,11212,11211,11210,11209,11208,11207,11206,11205,11204,11203,11201]
    queens_zip = [11451,11436,11435,11434,11433,11432,11429,11428,11427,11426,
                  11423,11422,11421,11420,11419,11418,11417,11416,11415,11414,11413,11412,11411,11385,11379,
                  11378,11377,11375,11374,11373,11372,11369,11368,11367,11366,11365,11364,11363,
                  11362,11361,11360,11359,11358,11357,11356,11355,11354,11351,11109,11106,11105,11104,11103,
                  11102,11101,11004]
    if x in m_zip + brooklyn_zip + queens_zip:
        return 1
    else:
        return 0


def point_in_zip(x):
    """
    validate if interest coordinate is within analytic region.
    
    Input a coordinate pair (lat, long)
    return 1 if coordinate in analytic area, 0 otherwise.
    """
    point = Point(x[0],x[1])
    y = None
    for ind,val in enumerate(gpd_zip['geometry']):
        if point.within(val):
            y = int(gpd_zip['ZIPCODE'].iloc[ind])
    return y


def recombine_zip(x):
    """
    Combine overlapped zip in New York.
    
    Input: a zipcode
    return the parent zipcode.
    """
    overlap_zip = {10118: 10001, 10119: 10001, 10120: 10001, 10121: 10001, 10122: 10001, 10123: 10001, 10041: 10004, 10275: 10004,
                   10043: 10005, 10081: 10005, 10203: 10005, 10259: 10005, 10260: 10005, 10265: 10005, 10270: 10005, 10271: 10005,
                   10286: 10005, 10278: 10007, 10279: 10007, 10047: 10010, 10158: 10016, 10165: 10017, 10166: 10017, 10167: 10017,
                   10168: 10017, 10169: 10017, 10170: 10017, 10171: 10017, 10172: 10017, 10173: 10017, 10174: 10017, 10175: 10017,
                   10176: 10017, 10177: 10017, 10178: 10017, 10097: 10019, 10103: 10019, 10104: 10019, 10105: 10019, 10106: 10019,
                   10107: 10019, 10111: 10019, 10020: 10019, 10112: 10019, 10162: 10021, 10055: 10022, 10151: 10022, 10152: 10022,
                   10153: 10022, 10154: 10022, 10155: 10022, 10096: 10036, 10110: 10036, 10196: 10036, 10045: 10038, 10080: 10048,
                   10285: 10281, 10069: 10023, 11451: 11433, 10115: 10027, 11109:11101}
     
    if x in overlap_zip.keys():
        return overlap_zip[x]
    if x in overlap_zip.values():
        return x
    else:
        return x

def verify_zip(x,y):
    """
    aggregate function of zipcode verification.
    
    Input: a pair of coordinate lat,long
    return the parent zipcode.
    """
    if x and isinstance(x,int) and valid_zip(x)==1:
        return x
    elif y and point_in_zip(y):
        
        return point_in_zip(y)      
        
    else:
        return None
        
def get_date_pred():
    
    """
    Get current datetime, month and day.

    """
    
    date_now = dt.datetime.now()
    date_pred = [date_now - dt.timedelta(days=1)+dt.timedelta(days=i) for i in range(8)]
    month_pred = [item.month for item in date_pred]
    day_pred = [item.day for item in date_pred]
    
    return date_pred,month_pred,day_pred

    

def get_weather_data(lat='40.761440',lng='-73.981806'):
    """
    get today's weather from Darksky API.
    
    Input: a pair of coordinate lat,long
    return the the weather of target location.
    """
    key ='********************************'
    x = pd.DataFrame()
    unix_now = int((dt.datetime.now()- dt.datetime(1970,1,1)).total_seconds())
    for time in range(unix_now-86400, unix_now+604800, 86400):
        rsp = rq.get('https://api.darksky.net/forecast/{}/{},{},{}'.format(key, lat, lng, time))
        rsp_json = json.loads(rsp.text)
        row = json_normalize(rsp_json["daily"]['data'])
        x = x.append(row)
       
    x = x[['icon','apparentTemperatureHigh','apparentTemperatureLow','cloudCover','humidity','precipProbability',
                 'pressure','visibility','windBearing','windGust','windSpeed']].reset_index(drop=True)
    return x

def update_tripsum(zip_input,checkin_trip,month_pred):

    """
    Get taxi trips of a certain month for prediction purpose
    Note: if the month was not included in the train data, trip number of 
            adjacent month will be used for prediction.
    """
    
    tripsum = []
    for item in month_pred:
        if item in [4,5,6,7,8,9,10,11,12]:
            tripsum.append(np.mean(checkin_trip[(checkin_trip['zip_code']==zip_input) & 
                                           (checkin_trip['month']==item)]['trip_sum']))
        elif item == 1:
            tripsum.append(np.mean(checkin_trip[(checkin_trip['zip_code']==zip_input) & 
                                           (checkin_trip['month']==12)]['trip_sum']))
        elif item == 2:
            tripsum.append(np.mean(checkin_trip[(checkin_trip['zip_code']==zip_input) & 
                                           (checkin_trip['month']==12)]['trip_sum']))
        elif item == 3:
            tripsum.append(np.mean(checkin_trip[(checkin_trip['zip_code']==zip_input) & 
                                           (checkin_trip['month']==4)]['trip_sum']))
    return tripsum
    


    
def compile_test_data(zip_input,weather_pred,checkin_trip, month_pred, day_pred):
               
    df_test = checkin_trip[checkin_trip['zip_code']==zip_input][0:8].reset_index(drop=True)
    df_test['month'] = month_pred
    df_test['day'] = day_pred
    df_test['trip_sum'] = update_tripsum(zip_input,checkin_trip,month_pred)
    df_test[['icon','apparentTemperatureHigh','apparentTemperatureLow','cloudCover','humidity','precipProbability',
                         'pressure','visibility','windBearing','windGust','windSpeed']] = weather_pred[['icon','apparentTemperatureHigh','apparentTemperatureLow','cloudCover','humidity','precipProbability',
                         'pressure','visibility','windBearing','windGust','windSpeed']]
    
    return df_test
