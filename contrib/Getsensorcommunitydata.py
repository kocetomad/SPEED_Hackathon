#!/usr/bin/env python3
import argparse
import requests
import json
import pandas as pd
from dateutil.parser import parse
from os.path import isfile
# define functions, classes, etc.

def getarchive( uri, filename ):
    more = ''
    if (isfile(filename)):
        # read from file

        print('File Exists - ' + filename)
        more = open(filename, 'r').read()
        if more != '':
            # read 
            pass
        else:
            print('no values failed.')
    else :
        
        print('No File GET - ', uri)
        r = requests.get(uri, allow_redirects=True)
        if (r.status_code != 200):
            open(filename, 'wb').write(r.content)
            print('No remote archive failed.')
        else :
            open(filename, 'wb').write(r.content)
        more = r.content
    return more

def getsensorsinarea(glat, glong, dist=10 ):
    # get the last readings, this my miss sensors from historical datasets which are down.
    # the distance is in km and create a boundinf square of double the distance across form
    # the latlog. (THIS HAS NOT BEEN TESTED)

   
    filename = 'data.24h.json'
    uri = 'https://data.sensor.community/static/v2/' + filename
    sensorreads =  getarchive(uri,filename)
    with open(filename) as hourjson:
        data = json.load(hourjson)
    df = pd.json_normalize(data)

    # extract locations
    # locs = pd.DataFrame(df['location'].tolist())
    
    # Calculate distance to latlong from km to deg
    deglat = 111 # km
    deglong = 85 # km (approx for europe)
    deglatr = dist / deglat
    deglongr = dist / deglong
    glatN = glat + deglatr
    glatS = glat - deglatr
    glongW = glong - deglongr
    glongE = glong + deglongr
    # this is the bounds of teh sensors to find. 
    #print('longr = '+ str(deglongr) +' :::: longE = ' + str(glongE) + " : longW = " + str(glongW))
    #print('latr = ' + str(deglatr)+ ' :::: latN = ' + str(glatN) + " : latS = " + str(glatS))   
    
    ##
    df['location.latitude'] = df['location.latitude'].astype(float) 
    df['location.longitude'] = pd.to_numeric(df['location.longitude'], errors='coerce')
    
    # select the distance around the location to identify the sensors
    sensors = df.loc[
             (df['location.latitude'] >= glatS) & (df['location.latitude'] <= glatN)
            & (df['location.longitude'] >= glongW) & (df['location.longitude'] <= glongE)
            ]

    return sensors[['id','location.id', 'location.longitude', 'location.latitude', 'location.indoor', 'sensor.sensor_type.name']]

def gettemporalreadings(tbegin, tend, sensors):
    # Use the luftdaten archive, to get the 
    archive = 'http://archive.sensor.community/'
    # dates in the format '<YYYY>-<MM>-<DD>/<YYYY>-<MM>-<DD>_<SENSORTYPE>_sensor_<SENSORID>.csv'
    # the sensors
    day = pd.to_datetime(tbegin)
    dayend = pd.to_datetime(tend)
    while (day < dayend):
        datestr = day.to_pydatetime().strftime('%Y-%m-%d')
        for id ,sensor in sensors.iterrows():
            filename = datestr + '_' + sensor['sensor.sensor_type.name'].lower() + '_sensor_' + str(sensor['location.id']) + '.csv'
            uri = archive +  datestr + '/' + filename
            #print(sensor['location.indoor'])
            print(uri)
            # Use this to get the archive, it will backup to a local copy.
            #print(getarchive(uri, filename))
        
        day=day+pd.DateOffset(days=1)
    print('done')
    #return sensorreadings

def main():

    sensors = getsensorsinarea(57.1368,-2.0906,10)
    print(sensors.count())
    #print(sensors)
    gettemporalreadings('2020-02-10', '2020-02-20', sensors)

# executes when your script is called from the command-line
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    #
    # define each option with: parser.add_argument
    #
    args = parser.parse_args() # automatically looks at sys.argv
    #
    # access results with: args.argumentName
    #
    main()
