from app import app
import os
import json

import requests
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    key = os.environ.get('API_KEY',"")
    if key == "":
        return "api error"

    req = requests.get("https://developer.cumtd.com/api/v2.2/json/GetVehicles?key=" + key)
    data = req.json()

    ret = list()
    avg_lat = 0
    avg_lon = 0
    act_len = 0
    for vehicle in data['vehicles']:
        ret.append("{lat: " + str(vehicle['location']['lat']) + ", lng: " + str(vehicle['location']['lon']) + "}")
        if abs(vehicle['location']['lon']) > 0.1: 
            avg_lon += vehicle['location']['lon']
            avg_lat += vehicle['location']['lat']
            act_len += 1
        else:
            print('caught')
        print (vehicle['location']['lon'], vehicle['location']['lat'])
    avg_lat /= act_len
    avg_lon /= act_len
    print(avg_lon, avg_lat)

    return render_template("map.html",points = ret, lon = avg_lon, lat = avg_lat)