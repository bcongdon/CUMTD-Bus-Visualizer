from app import app
import os
import json

import requests

@app.route('/')
@app.route('/index')
def index():
    key = os.environ.get('API_KEY',"")
    if key == "":
        return "api error"

    req = requests.get("https://developer.cumtd.com/api/v2.2/json/GetVehicles?key=" + key)
    data = req.json()

    ret = ""
    for vehicle in data['vehicles']:
        ret += "ID: " + vehicle['vehicle_id'] + " "
        ret += "Location: " + str(vehicle['location']['lat']) + "," + str(vehicle['location']['lon'])
        ret += "<br>"

    return ret