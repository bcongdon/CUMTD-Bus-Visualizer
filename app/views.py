from app import app
import json
import datetime

from bus_client import BusClient
from flask import render_template

client = BusClient()

@app.route('/')
@app.route('/index')
def index():
    global client
    data = client.get_busses()
    if data is not None:
        return render_template("map.html",points = data[0], lon = data[1], lat = data[2], count = data[3])
    else:
        return "Error"

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404