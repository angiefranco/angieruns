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
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


activites_url = "https://www.strava.com/api/v3/athlete/activities"

def get_access_token():
    auth_url = "https://www.strava.com/oauth/token"
    CLIENT_ID=os.environ.get('CLIENT_ID')
    CLIENT_SECRET=os.environ.get('CLIENT_SECRET')
    REFRESH_TOKEN=os.environ.get('REFRESH_TOKEN')
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': "refresh_token",
        'f': 'json'
    }

    r=requests.post(auth_url,data=payload,verify=False)
    access_token = r.json()['access_token']
    return access_token

def get_my_dataset(access_token):
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    my_dataset = requests.get(activites_url, headers=header, params=param).json()
    return my_dataset

def get_data(my_dataset, last_run):
    #distance in mi
    factor=1609
    distance=float((my_dataset[last_run]["distance"])/factor)
    distance=round(distance,2)
    distance=str(distance)+ " mi"

    #pace in mins per mile
    tot_seconds=my_dataset[last_run]["moving_time"]
    tot_distance=my_dataset[last_run]["distance"]
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


def get_date(my_dataset, last_run):
    mydate=my_dataset[last_run]['start_date']
    date_obj = datetime.strptime(mydate, "%Y-%m-%dT%H:%M:%SZ")
    formatted_date = date_obj.strftime("%B %d, %Y")
    return formatted_date

access_token=get_access_token()
my_dataset=get_my_dataset(access_token)

for index,workout in enumerate(my_dataset):
    if workout['sport_type'] == 'Run':
        last_run=index
        distance, pace, time=get_data(my_dataset, last_run)
        date=get_date(my_dataset,last_run)
        print(distance,pace,time)
        break
    



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


