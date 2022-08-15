#pip install requests OR python -m pip install requests
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

os.environ['TZ']='UTC'
now = datetime.datetime.now() # http://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/

now_60d_back = now + relativedelta(days=-60)

#influxdb access data
host = "192.168.0.104"
port = "8086"
user = "energy"
password = "energypassword"
dbname = "energy"
client = InfluxDBClient(host, port, user, password, dbname)

meters = ["Haus", "WP"]

for meter in meters:

   print(meter + "....")

   query = "SELECT * from energy_current WHERE meter = '" + meter + "'  AND time < '"  + str(now_60d_back) + "'"
   response = client.query(query)
   print(str(len(response)) + " point(s) found")
#   print(response)

   query = "DELETE from energy_current WHERE meter = '" + meter + "'  AND time < '"  + str(now_60d_back) + "'"
   response = client.query(query)
#   print(str(len(response)))
#   print(response)
