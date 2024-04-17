'''Connects all of the components together. Gets the user input (for now, its in a while True loop.) and calculates everything based on it'''

import logging
from geocoding import Geocoding_Manager
from earthquakes import Earthquake_Manager
from database import Database_Manager

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(msg)s')

geocoder = Geocoding_Manager()
earthquake = Earthquake_Manager()
db = Database_Manager()

while True:
    data = geocoder.geocode(input('Input an address/city/country name: '))
    res = db.insert_data(earthquake.find_earthquake(data))
    if res:
        logging.info('Success! The data about the earthquake has been written in the table.')
    else:
        logging.info('Error!')
