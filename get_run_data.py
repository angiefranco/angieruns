#!/usr/bin/env/python3
from datetime import datetime
import math
import json


with open('strava_data.txt', 'r') as file:
    my_dataset=json.load(file)


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
    if pace_secs < 10:
        pace_secs="0"+str(pace_secs)
    pace = str(pace_mins) + ":" + str(pace_secs) + " /mi"
 
    #total run time
    tot_mins, tot_secs = divmod(tot_seconds,60)
    if tot_mins > 60:
        tot_hours, tot_mins = divmod(tot_mins,60)
        time=str(math.trunc(tot_hours)) + "h " + str(math.trunc(tot_mins)) + "s"
        return distance, pace, time
    
    time= str(math.trunc(tot_mins)) + "m " + str(math.trunc(tot_secs)) + "s"
    
    # #get date
    # mydate=my_dataset[last_run]['start_date']
    # date_obj = datetime.strptime(mydate, "%Y-%m-%dT%H:%M:%SZ")
    # formatted_date = date_obj.strftime("%B %d, %Y")
    
    return distance,pace,time


def get_date(my_dataset, last_run):
    mydate=my_dataset[last_run]['start_date']
    date_obj = datetime.strptime(mydate, "%Y-%m-%dT%H:%M:%SZ")
    formatted_date = date_obj.strftime("%B %d, %Y")
    return formatted_date

stats_dic={}
for index,workout in enumerate(my_dataset):
    if workout['sport_type'] == 'Run':
        last_run=index
        distance, pace, time=get_data(my_dataset, last_run)
        date=get_date(my_dataset,last_run)
        di="distance"+str(index)
        p="pace"+str(index)
        t="time"+str(index)
        dt="date"+str(index)
        stats_dic[di]=distance
        stats_dic[p]=pace
        stats_dic[t]=time
        stats_dic[dt]=date
