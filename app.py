from flask import Flask, render_template, request, redirect

import pandas as pd
import datetime as dt
import static.module.processFunc as proc
import static.module.predictFunc as pred


## Input resource data        
checkin_trip = pd.read_csv('static/checkin_trip_0828.csv')
checkin_trip.drop('Unnamed: 0',axis=1,inplace=True)
## get real time date and weather
today = dt.datetime.now().strftime('%Y/%m/%d')
date_pred,month_pred,day_pred = proc.get_date_pred()
weather_pred = proc.get_weather_data()



app = Flask(__name__)


app.vars={}

@app.route('/',methods=['GET','POST'])
def index():

    apparentTemperature = '{:.0f}'.format(sum(weather_pred.loc[1][1:3])/2)
    icon = weather_pred.loc[1][0].replace('-',' ')
    
    labels = [item.strftime("%b-%d") for item in date_pred]
    values = [0, 0, 0, 0, 0, 0, 0, 0]
    if request.method == 'GET':
        return render_template('index.html',checkin_num = 0,volume_proj = 0,temp = apparentTemperature,date = today,zipdisplay = "",
                                            weather_icon = icon,labels = labels, values = values)
    

@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/predict_action',methods=['POST'])
def predict_action():
    
    zip = 0
    lng = 0
    lat = 0   
    
    if request.form['zip']:
        try:
            app.vars['zip_input'] = zip = int(request.form['zip'])
        except:
            pass
            
    elif (request.form['lat'] and request.form['lng']):
        try:
            app.vars['lat_input'] = lat = float(request.form['lat'])
            app.vars['lng_input'] = lng = float(request.form['lng'])

        except:
            return render_template('404.html')
            

            
    zip_input = proc.verify_zip(zip,[lng,lat])
         
      
    f = open('visit_record.txt','a')
    f.write('ZIPCODE request: %s\n'%(zip_input))
    f.close()
    
    
    if zip_input:
        df_test = proc.compile_test_data(zip_input,weather_pred,checkin_trip, month_pred, day_pred)
                           
        df_test['checkin_pred'] = pred.rfr_predict(df_test.drop('checkin_sum',axis=1))
        
        checkin_pred = df_test.loc[1][-1]
        
        
        apparentTemperature = '{:.0f}'.format(sum(weather_pred.loc[1][1:3])/2)
        icon = weather_pred.loc[1][0].replace('-',' ')        
        labels = [item.strftime("%b-%d") for item in date_pred]
        values = [item for item in df_test['checkin_pred']]
  
        
        return render_template('index.html',checkin_num ='{:.1f}'.format(checkin_pred),volume_proj='Developing',date = today,
                               zipdisplay = zip_input, temp = apparentTemperature,weather_icon = icon,labels = labels, values = values)
    else:
        return render_template('404.html')
    

    
if __name__ == '__main__':
  app.run(debug = True)
