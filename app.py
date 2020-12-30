from flask import Flask, render_template, url_for, request, redirect, jsonify
import os
import requests
from bs4 import BeautifulSoup
# import numpy as np
# import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    gunstock_html = requests.get("https://www.gunstock.com/on-snow/snow-report/")
    gunstock_soup = BeautifulSoup(gunstock_html.content, 'html.parser')

    trail_reports = gunstock_soup.find_all('article', class_="SnowReport-Trail")
    print(trail_reports[0])

    # This datastructure contains the image filename and its associated open state
    trails_status = {}

    for trail_report in trail_reports:
        trail_name = trail_report.find('h3', class_="SnowReport-feature-title").text
        
        trail_name = trail_name.replace(" ", "_").replace("'", "")
        trail_name += ".png"

        is_open = True if trail_report.find('i', class_='pti-open') != None else False
        print(trail_name + " : " + str(is_open))

        trails_status[trail_name] = is_open

    trails_status['Trigger_Chute.png'] = trails_status['Flintlock.png'] & trails_status['Upper_Trigger.png']
    trails_status['Flintlock_Chute.png'] = trails_status['Derringer.png']

    return render_template('index.html', trails_status=trails_status)