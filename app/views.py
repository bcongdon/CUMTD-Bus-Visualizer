from app import app
import os
import json
import datetime

import requests
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    data = get_busses()
    if data is not None:
        return render_template("map.html",points = data[0], lon = data[1], lat = data[2])
    else:
        return "Error"


def get_busses():
    key = os.environ.get('API_KEY',"")
    if key == "":
        print "Could not load API_KEY"
        return

    req = requests.get("https://developer.cumtd.com/api/v2.2/json/GetVehicles?key=" + key)
    data = req.json()

    ret = list()
    avg_lat, avg_lon, act_len = 0, 0, 0

    if not 'vehicles' in data:
        print "Data not in expected format"
        return

    for vehicle in data['vehicles']:
        if not 'trip' in vehicle:
            success = False
            return "JSON error"
        ret.append(vehicle)
        if abs(vehicle['location']['lon']) > 0.1: 
            avg_lon += vehicle['location']['lon']
            avg_lat += vehicle['location']['lat']
            act_len += 1
        else:
            print('caught')
    avg_lat /= act_len
    avg_lon /= act_len
    return (ret,avg_lon,avg_lat,True)