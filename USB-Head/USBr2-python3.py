# sudo apt-get install python
# sudo apt-get install python-pip
# pip install requests influxdb pyserial pyyaml
# OR 
# python -m pip install requests influxdb pyserial pyyaml

import requests
import json
import os
import os.path
import calendar
import sys
import io
import serial
import time
import yaml
import codecs
from influxdb import InfluxDBClient

def UTC_to_epoch(timestamp):
    pattern = '%Y-%m-%dT%H:%M:%SZ'
    epoch = calendar.timegm(time.strptime(timestamp, pattern))
    return epoch

def get_data(search, data, offset, length):
    pos = data.find(search)
    if (pos != -1):
        pos = pos + len(search) + offset
        value = data[pos:pos + length]
        print("value: " + str(value))
        return(str(int(value, 16)))
	
def cli_help():
  print("Usage: USBr2.py [-influxdb]")
  exit(1)
  
USB_device = "/dev/ttyUSB0"

meter = "2-way"

arg_influxdb = False
	
if(len(sys.argv) == 2):
   if(sys.argv[1] == '-influxdb'):
       arg_influxdb = True
   else:
       cli_help()
    
#
# influxdb access data
#
influxdb_host = '192.168.0.104'
influxdb_port = '8086'
influxdb_user = 'energy'
influxdb_password = 'energypassword'
influxdb_dbname = 'energy'

client = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_dbname)

#
# open USB to read
#
port = serial.Serial(
	port=USB_device,
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

# 
# get the result that we are interested in
#

start = '1b1b1b1b01010101'
end = '1b1b1b1b1a'

data = ''
total_bezug=''
total_einspeisung = ''
loop = 0

while ((total_bezug == '') and(total_einspeisung == '') and (loop <= 3)):
    inner_loop = 0
    while(True):
        inner_loop = inner_loop + 1
        char = port.read()
        data = data + codecs.encode(char, "hex").decode('ascii')
        pos = data.find(start)
        if (pos != -1):
            data = data[pos:len(data)]
            pos = data.find(end)
        if (pos != -1):
            print("inner_loop: " + str(inner_loop))
            break

    print("Loop: " + str(loop))
    print(data)
    print("-----")
    
    total_bezug = get_data('070100010800ff', data, 20, 16)
    #total_bezug = get_data('070100010802ff', data, 14, 16)
    print("Gesamt Bezug: " + str(total_bezug))
    print("-----")
    
    total_einspeisung = get_data('070100020800ff', data, 20, 16)
    #total_einspeisung = get_data('070100020801ff', data, 14, 16)
    print("Gesamt Einspeisung: " + str(total_einspeisung))

    loop = loop + 1
		
#
# get current time
#
os.environ['TZ']='UTC'
timestamp = calendar.timegm(time.gmtime()) * 1000000000

#
# create json_body 'total'
#


json_body = [
              {
                  "measurement": "energy",
                  "tags": {
                      "meter": meter
                  },
                  "time": timestamp,
                  "fields": {
                      "Total Bezug": float(total_bezug),
                      "Total Einspeisung": float(total_einspeisung)
                  } 
              }
          ]
			



if(arg_influxdb == True):
    print(json.dumps(json_body, indent=4, sort_keys=True))    
    client.write_points(json_body)

