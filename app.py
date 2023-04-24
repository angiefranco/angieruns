from flask import Flask, render_template, request
import requests
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
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import subprocess
from datetime import datetime
load_dotenv()


app = Flask(__name__)
#app.config['SERVER_NAME'] = 'yourcustomdomain.com'


@app.route("/deploy", methods=['POST'])
def deploy():
    if request.method == 'POST':
        subprocess.call(['/home/ec2-user/deploy.sh'])
        return 'Deployment Successful!'


with open("strava_api.py") as strava:
    exec(strava.read())

@app.route("/")
def angieruns():

    #get the live amount raised from website
    url='https://hope.drugfree.org/endurance-teams/angieruns'
    response= requests.get(url)
    soup=BeautifulSoup(response.content, 'html.parser')
    progress_message=soup.find(id="NewProgressAmtRaised").get_text() #string with amount raised and goal
    progress = int(re.search('\$(\d+(?:,\d+)*)', progress_message).group(1).replace(',', ''))
    goal = 3500
    progress_percentage = progress / goal * 100

    return render_template('home.html', distance=distance, pace=pace, time=time, date=date, progress=progress, goal=goal, progress_percentage=progress_percentage, progress_message=progress_message)

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)
