'''Contains the class with methods used for finding the most recent earthquake in 100 miles distance of the given coordinates.'''

import requests
import json
import logging
from configparser import ConfigParser

reader = ConfigParser()
reader.read('config.ini')

logger = logging.getLogger('EARTHQUAKES')

class Earthquake_Manager:
    def __init__(self):
        self.url = 'https://everyearthquake.p.rapidapi.com/latestEarthquakeNearMe'

        self.headers = {
        "X-RapidAPI-Key": reader['USER_DETAILS']['API_KEY'],
        "X-RapidAPI-Host": "everyearthquake.p.rapidapi.com"
        }
    
    def segregate_info(self, info):
        '''One of the keys in the response that the API gives is called "Title", which contains the main info about the earthquake.
        This function recieves the value binded to that key and seperates the data into two parts: magnitude of the earthquake and the location.'''
        split_result = info.split('-')
        return (split_result[0], split_result[1].lstrip())

    def send_req(self, cords):
        '''Sends a request to the API.'''

        if not cords['lat'] and not cords['lon']:
            return cords
        
        params = {
            'latitude' : cords['lat'],
            'longitude' : cords['lon']
        }

        res = requests.get(self.url, headers = self.headers, params = params)
        return res.content


    def find_earthquake(self, cords):
        '''We pass the coordinates returned by geocode() to this method. It finds the most recent earthquake
           and returns the structured data. The returned data will be used in the Database_Manager class.'''
        if len(cords) == 4:
            return cords
        res = self.send_req(cords)
        if not res:
            return 'Couldnt find data!'
        data = json.loads(res)
        info = self.segregate_info(data['data'][0]['title'])

        return {**cords, 'magnitude' : info[0], 'location' : info[1],'date' : data['data'][0]['date'], 'info_url' : data['data'][0]['url']}



