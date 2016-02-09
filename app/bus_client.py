import os
import requests
import json

from datetime import timedelta
from datetime import datetime

class BusClient():

	last_request = None
	data = None

	def get_busses(self):
		if self.last_request is None or (self.last_request - datetime.today()) > timedelta(minutes=1):
			self.data = self.get_busses_raw()
			self.last_request = datetime.today()
		else:
			print "Using cached data; too soon to make new request"
		return self.data

	def get_busses_raw(self):
	    key = os.environ.get('API_KEY',"")
	    if key == "":
	        print "Could not load API_KEY"
	        return

	    print "Making request to CUMTD"
	    req = requests.get("https://developer.cumtd.com/api/v2.2/json/GetVehicles?key=" + key)
	    data = req.json()

	    ret = list()
	    avg_lat, avg_lon, act_len = 0, 0, 0

	    if not 'vehicles' in data:
	        print "Data not in expected format"
	        return

	    count = 0
	    for vehicle in data['vehicles']:
	        if not 'trip' in vehicle:
	            success = False
	            return "JSON error"
	        ret.append(vehicle)
	        if abs(vehicle['location']['lon']) > 0.1: 
	            avg_lon += vehicle['location']['lon']
	            avg_lat += vehicle['location']['lat']
	            act_len += 1
	            count += 1
	        else:
	            print('caught')
	    avg_lat /= act_len
	    avg_lon /= act_len
	    return (ret,avg_lon,avg_lat,count)