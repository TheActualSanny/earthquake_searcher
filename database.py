'''Manages EVERYTHING in writing/reading/modifying the partitioned database.'''

import psycopg2
import logging
from configparser import ConfigParser

reader = ConfigParser()
reader.read('config.ini')

class Database_Manager:

    def connector(self):
        '''Connects to the database (initializes a connection and a cursor). It is used in other methods along with disconnect(), in order to avoid
        memory leakage. '''

        self._conn = psycopg2.connect(
            host = reader['DATABASE_DETAILS']['HOST'],
            user = reader['DATABASE_DETAILS']['USER'],
            password = reader['DATABASE_DETAILS']['PASS'],
            database = reader['DATABASE_DETAILS']['DB']
        )
        self._curr = self._conn.cursor()
        self._curr.execute('''CREATE TABLE IF NOT EXISTS earthquake_logs(
                           id SERIAL PRIMARY KEY,
                           location text,
                           latitude real,
                           longitude real,
                           magnitude text,
                           date text,
                           info_link text)
                           ''')

        self._curr.execute('''CREATE TABLE IF NOT EXISTS earthquake_errors(
                           id SERIAL PRIMARY KEY,
                           location text,
                           date_sent text
        )''')

    def disconnect(self):
        self._curr.close()
        self._conn.close()

    def insert_data(self, data):
        '''Gets the data returned from Earthquake_Manager() class and writes it into the table.
           For now, it checks the data by the length. (if the length of the dict is 4, there was an error and it
           writes it in earthquake_errors table.)'''

        self.connector()
        if len(data) == 4:
            with self._conn:
                self._curr.execute('INSERT INTO earthquake_errors(location, date_sent) VALUES(%s, %s)', (data['location'], data['sent_date']))
            self.disconnect()
            return None
        
        else:
            with self._conn:
                self._curr.execute('''INSERT INTO earthquake_logs(location, latitude, longitude, magnitude, date, info_link)
                                    VALUES(%s, %s, %s, %s, %s, %s)''', tuple(data.values()))
            self.disconnect()
            return 1
        

