import requests
import json
import os

import calendar
import time
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import pprint

from influxdb import InfluxDBClient

now = datetime.datetime.now()

#
# influxdb access data
#
influxdb_host = '192.168.0.104'
influxdb_port = '8086'
influxdb_user = 'energy'
influxdb_password = 'energypassword'
influxdb_dbname = 'energy'

client = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_dbname)

meters = ["Haus", "WP"]

for meter in meters:
    # while loop to cycle over intersting dates
    this_date = date(2017,1,1)
    today = date(now.year, now.month, now.day)
    while(this_date < today):
        query = "SELECT Total from energy WHERE meter = '" + meter + "' AND time > '" + str(this_date) + "T00:00:00Z' AND time < '"  + str(this_date) + "T23:59:59Z'"
        result = client.query(query)
        result_points = list(result.get_points(measurement='energy'))
        l = len(result_points)
        if(l>0):
            print(meter + ": " +str(this_date) + " " + str(l))
        this_date = this_date + relativedelta(days=1)

    #this_date = date(2017,4,14)
    #query = "DELETE from energy WHERE meter = '" + meter + "' AND time > '" + str(this_date) + "T00:00:00Z' AND time < '"  + str(this_date) + "T23:59:59Z'"
    #result = client.query(query)
    #print(result)
