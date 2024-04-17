EARTHQUAKE SEARCHER APPLICATION


To use the program, launch the main.py file. For now, the whole thing will run in an infinite while loop (In the future I will add a flask application).
Then input a city/country/address and wait a bit for the API responses. The result will be printed (If data was found or not) and will also be written in the
database.



DATABASE

the database is called: earthquake_data

Currently, it has 2 tables: earthquake_logs and earthquake_errors
If data was not found for the given address (Random text was sent as the parameter to the API), The given location and the time of execution will be inserted in earthquake_errors.
If thats not the case and everything finished successfully, the data will be written into earthquake_logs, which has 7 fields:

id: primary key and a serial number,

location: the location returned from the API,

latitude and longitude: real numbers,

magnitude:  Recorded magnitude of the earthquake,

date: Date when the earthquake was recorded
