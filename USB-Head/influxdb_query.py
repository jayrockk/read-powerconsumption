# sudo apt-get install python
# sudo apt-get install python-pip
# pip install requests influxdb pyserial 
# OR 
# python -m pip install requests influxdb pyserial

import pprint
import json
from influxdb import InfluxDBClient

#
# influxdb access data
#
influxdb_host = '192.168.0.104'
influxdb_port = '8086'
influxdb_user = 'energy'
influxdb_password = 'energypassword'
influxdb_dbname = 'energy'

#
# run command
#

client = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_dbname)

query = "SELECT * FROM energy_current WHERE meter = 'PV' AND time > '2017-10-09 06:32:00' AND time < '2017-10-09 06:33:00'"
response = client.query(query)
pprint.pprint(response)
print("\n")

query = "DELETE FROM energy_current WHERE meter = 'PV' AND time > '2017-10-09 06:32:00' AND time < '2017-10-09 06:33:00'"
response = client.query(query)
pprint.pprint(response)
print("\n")

#query = "SELECT * FROM energy WHERE meter = 'PV' AND time =  1507507160000000000"
#response = client.query(query)
#pprint.pprint(response)

