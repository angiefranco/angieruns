#!/usr/bin/env/python3
import requests
import urllib3
import json
import math
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import folium
import polyline
import base64
from tqdm import tqdm
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


activites_url = "https://www.strava.com/api/v3/athlete/activities"

def get_access_token():
    auth_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': "105510",
        'client_secret': 'f62aa8c820a2c947fdc16b5c89ed357f9360e8c0',
        'refresh_token': '61879cc0767f0188e1ffdbd8306d0cacdf7d4cbc',
        'grant_type': "refresh_token",
        'f': 'json'
    }

    r=requests.post(auth_url,data=payload,verify=False)
    access_token = r.json()['access_token']
    return access_token

def get_my_dataset(access_token):
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 1, 'page': 1}
    my_dataset = requests.get(activites_url, headers=header, params=param).json()
    return my_dataset

def get_data(my_dataset):
    #distance in mi
    factor=1609
    distance=float((my_dataset[0]["distance"])/factor)
    distance=round(distance,2)
    distance=str(distance)+ " mi"

    #pace in mins per mile
    tot_seconds=my_dataset[0]["moving_time"]
    tot_distance=my_dataset[0]["distance"]
    seconds_per_mile=(tot_seconds/tot_distance)*1000*1.609
    pace_mins, pace_secs = divmod(seconds_per_mile,60)
    pace_mins=math.trunc(pace_mins)
    pace_secs=math.trunc(round(pace_secs,0))
    pace = str(pace_mins) + ":" + str(pace_secs) + " /mi"
 
    #total run time
    tot_mins, tot_secs = divmod(tot_seconds,60)
    if tot_mins > 60:
        tot_hours, tot_mins = divmod(tot_mins,60)
        time=str(math.trunc(tot_hours)) + "h " + str(math.trunc(tot_mins)) + "s"
        return distance, pace, time
    
    time= str(math.trunc(tot_mins)) + "m " + str(math.trunc(tot_secs)) + "s"
    return distance,pace, time

def get_map(my_dataset):
    activity=pd.json_normalize(my_dataset)
    activity['map.polyline']=activity['map.summary_polyline'].apply(polyline.decode)
    return activity

# define function to get elevation data using the open-elevation API
def get_elevation(latitude, longitude):
    base_url = "https://api.open-elevation.com/api/v1/lookup"
    payload = {'locations': f'{latitude},{longitude}'}
    r = requests.get(base_url, params=payload).json()['results'][0]
    return r['elevation']


access_token=get_access_token()
my_dataset=get_my_dataset(access_token)
distance, pace, time=get_data(my_dataset)
# activity=get_map(my_dataset)

# get elevation data
# elevation_data = list()
#elevation = [get_elevation(coord[0], coord[1]) for coord in activity['map.polyline']]
#elevation_data.append(elevation)

# elevation=get_elevation(40.75922, -73.99844)
# print("elevation success")
# print("\n\n")
# print(elevation)

# add elevation data to dataframe
# activity['map.elevation'] = elevation_data

# my_ride = activity.iloc[0, :] 
# # plot ride on map
# centroid = [
#     np.mean([coord[0] for coord in my_ride['map.polyline'][0]]), 
#     np.mean([coord[1] for coord in my_ride['map.polyline'][0]])
# ]
# m = folium.Map(location=centroid, zoom_start=10)
# folium.PolyLine(my_ride['map.polyline'], color='red').add_to(m)
# map_html = m._repr_html_()
# print(map_html)

