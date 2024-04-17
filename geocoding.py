'''Gets the latitude and longitude of the input Country, manages the JSON Data...'''

import requests
import json
import logging
from configparser import ConfigParser
from datetime import datetime

logger = logging.getLogger('GEOCODING')
config = ConfigParser()
config.read('config.ini')

class Geocoding_Manager:
    def __init__(self):
        self.url = 'https://nominatim.openstreetmap.org/search'

        self.headers = {
            'User-Agent' : config['USER_DETAILS']['AGENT']
        }
    
    def send_req(self, location):
        '''Sends the request to the API. The given location is passed as a parameter and the JSON response data is returned.'''

        self.params = {
            'q' : location,
            'format' : 'json'
        }
        res = requests.get(self.url, headers = self.headers, params = self.params)
        return res.content
    
    
    def geocode(self, location):
        '''Simply extends the send_req() method and returns a dictionary of the latitude and longitude of the given country/address.
           If there are no coordinates found fro the given location, it returns a dict of only the location and current date to write in the database.
           (Other fields are still there, but their values are equal None objects). '''

        res = self.send_req(location)
        if  res.decode() == '[]':
            return {'location' : location, 'lat' : None, 'lon' : None, 'sent_date' : str(datetime.now())}
        data = json.loads(res)
        return {'location': location, 'lat': data[0]['lat'], 'lon' : data[0]['lon']}

