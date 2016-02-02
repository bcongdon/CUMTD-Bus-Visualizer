from app import app
import os

import requests

key = ""

@app.route('/')
@app.route('/index')
def index():
    with app.open_resource("static/api_key") as f:
        key = f.read()

    req = requests.get("https://developer.cumtd.com/api/v2.2/json/GetVehicles?key=" + key)
    data = req.json()

    for vehicle in data['vehicles']:
        print "ID: " + vehicle['vehicle_id']
        print "Location: " + str(vehicle['location']['lat']) + "," + str(vehicle['location']['lon'])
        print

    return str(data)