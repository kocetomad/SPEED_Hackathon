#!/usr/bin/env python3

# this will fill the directory you call this from with CSV files from the sensor.community dataset then use them as an arvice 

import argparse
from pathlib import Path
import requests
import json
import pandas as pd
from dateutil.parser import parse
from os.path import isfile

# check if the files has been dwnloaded from a url, download and archive if not,
# or return arcchive if previously downloaded.
def getarchive( uri, filename ):
    more = ''
    if (isfile(filename)):
        # read from file

        print('File Exists - ' + filename)
        more = open(filename, 'r').read()
        if more != '':
            # read there is data in the file
            return filename
        else:
            # the file is empty
            print('no values - failed.')
    else :
        
        print('No File GET - ', uri)
        r = requests.get(uri, allow_redirects=True)
        if (r.status_code != 200):
            Path(filename).touch()
            print('No remote archive, failed to get ' + uri)
        else :
            open(filename, 'wb').write(r.content)
            return filename
    return ''

# find all sesnors currently reading in an area atound a geolocation,
# returns a dataframe with the sensor readings
def getsensorsinarea(glat, glong, dist=10 ):
    # get the last readings, this my miss sensors from historical datasets which are down.
    # the distance is in km and create a bounding square of double the distance across form
    # the latlog.

    filename = 'data.24h.json'
    uri = 'https://data.sensor.community/static/v2/' + filename
    archive = getarchive(uri,filename)
    if (archive == filename):
        with open(filename) as hourjson:
            data = json.load(hourjson)
        df = pd.json_normalize(data)

        # Calculate distance to latlong from km to deg this just selesct everything in a box
        # around the geolocation with a size of 2*dist
        deglat = 111 # km
        deglong = 85 # km (approx for europe)
        deglatr = dist / deglat
        deglongr = dist / deglong
        glatN = glat + deglatr
        glatS = glat - deglatr
        glongW = glong - deglongr
        glongE = glong + deglongr

        # this is the bounds of teh sensors to find. 
        #print('longr = '+str(deglongr)+' :::: longE = '+str(glongE)+" : longW = "+str(glongW))
        #print('latr = '+str(deglatr)+' :::: latN = '+str(glatN)+" : latS = "+str(glatS))   
        
        ##
        df['location.latitude'] = df['location.latitude'].astype(float) 
        df['location.longitude'] = pd.to_numeric(df['location.longitude'], errors='coerce')
        
        # select the distance around the location to identify the sensors
        sensors = df.loc[
                 (df['location.latitude'] >= glatS) & (df['location.latitude'] <= glatN)
                & (df['location.longitude'] >= glongW) & (df['location.longitude'] <= glongE)
                ]
    
        return sensors[['id','sensor.id', 'location.longitude', 'location.latitude', 'location.indoor', 'sensor.sensor_type.name']]
    else :
        return null

# will return a list of 3 dataframes of the sensor data over the time period 
def gettemporalreadings(tbegin, tend, sensors):
    # Use the luftdaten archive, to get the 
    archive = 'http://archive.sensor.community/'
    # dates in the format '<YYYY>-<MM>-<DD>/<YYYY>-<MM>-<DD>_<SENSORTYPE>_sensor_<SENSORID>.csv'
    # the sensors
    day = pd.to_datetime(tbegin)
    dayend = pd.to_datetime(tend)
    sds011files = []
    dht22files = []
    bme280files = []

    while (day < dayend):
        datestr = day.to_pydatetime().strftime('%Y-%m-%d')
        for id ,sensor in sensors.iterrows():
            if sensor['location.indoor']:
                indoor = '_indoor'
            else:
                indoor = ''
            filename = datestr + '_' + sensor['sensor.sensor_type.name'].lower() + '_sensor_' +  str(sensor['sensor.id']) + indoor + '.csv'
            uri = archive +  datestr + '/' + filename
            
            archivefile = getarchive(uri, filename)
            if archivefile != '':
                if sensor['sensor.sensor_type.name'] == 'SDS011':
                    sds011files.append(archivefile)
                elif sensor['sensor.sensor_type.name'] == 'DHT22':

                    dht22files.append(archivefile)
                elif sensor['sensor.sensor_type.name'] == 'BME280':
                    bme280files.append(archivefile)
        day=day+pd.DateOffset(days=1)

    #print(datafiles)
    read_csv = lambda x: pd.read_csv(x , sep=';')  
    sds011data = pd.concat(map(read_csv, sds011files))
    dht22data = pd.concat(map(read_csv, dht22files))
    bme280data = pd.concat(map(read_csv, bme280files))

    
    return (sds011data, dht22data, bme280data)

def main():

    # WARNING. there is no restriction on this, you could end up collecting 
    #   all data from the server is you set the bounds too large.
    
    glat = 57.1382
    glong = -2.0946
    gdist = 10 # km 1/2 length of bounding square
    
    startdate = '2020-02-10'
    enddate = '2020-01-19'

    sensors = getsensorsinarea(glat,glong,gdist)
    sensordataframes = gettemporalreadings('2020-02-10', '2020-02-20', sensors)

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
