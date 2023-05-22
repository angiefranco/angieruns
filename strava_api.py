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
from datetime import datetime, timedelta
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



# determine if it has been more than a day since the strava data was loaded
current_date=datetime.now()
a_day_ago=current_date - timedelta(hours=24)
last_modified_time = os.path.getmtime('strava_data.txt')
last_modified_datetime = datetime.fromtimestamp(last_modified_time)

if last_modified_datetime < a_day_ago:
    print("in if")
    access_token=get_access_token()
    my_dataset=get_my_dataset(access_token)
    my_dataset_json=json.dumps(my_dataset)
    with open('strava_data.txt','w') as file:
        file.write(my_dataset_json)
        print("wrote new data")

    

    