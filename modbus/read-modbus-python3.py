#
# This is a python3 script
#

#
# pip install modbus_tk
#


import os
import json
import calendar
import sys
import io
import time
import yaml
from influxdb import InfluxDBClient
import struct
import socket

pow2_48 = 281474976710656
pow2_32 = 4294967296
pow2_16 = 65536

def cli_help():
  print("Usage: read-modbus.py <Total|Current>")
  exit(1)

def read_modbus(ip, address, length):
    import modbus_tk
    import modbus_tk.defines as cst
    import modbus_tk.modbus_tcp as modbus_tcp

    result = "00"
    master = modbus_tcp.TcpMaster(host=ip, port=502, timeout_in_sec=5.0)
    try:
        result = master.execute(3, cst.READ_HOLDING_REGISTERS, address, length)
    except modbus_tk.modbus.ModbusError as exc:
        print("%s- Code=%d", exc, exc.get_exception_code())
    except socket.error as exc:
        print("%s- Code=%d", exc)
    finally:
        master.close()

    #return list(result)
    return result

def fourToupleRegister2int(input_t):

  result = input_t[0] * pow2_48 + input_t[1] * pow2_32 + input_t[2] * pow2_16 + input_t[3]

  return result
    

if(len(sys.argv)!=2):
    cli_help()

argument_1 = sys.argv[1]
 
if(argument_1=='Total'):
    print("Total")
    value_style='total'
elif(argument_1=='Current'):
    print("Current")
    value_style='current'
else:
    cli_help()	
	

#
# get current time
#
os.environ['TZ']='UTC'
timestamp = calendar.timegm(time.gmtime()) * 1000000000
	
#
# influxdb access data
#
influxdb_host = '192.168.0.104'
influxdb_port = '8086'
influxdb_user = 'energy'
influxdb_password = 'energypassword'
influxdb_dbname = 'energy'
 

output91 = read_modbus("192.168.2.91", 30513, 4)
output92 = read_modbus("192.168.2.92", 30513, 4)
output93 = read_modbus("192.168.2.93", 30845, 2)

wr1_total = float(fourToupleRegister2int(output91))/1000
wr2_total = float(fourToupleRegister2int(output92))/1000
batt_charge = float(output93[1])

print("WR1:  " + "{0:.2f}".format(wr1_total))
print("WR2:  " + "{0:.2f}".format(wr2_total))
print("SOC:  " + "{0:.0f}".format(batt_charge) + "%")

if(value_style=='total'):
    json_body = [
              {
                  "measurement": "energy",
                  "tags": {
                      "meter": "PV"
                  },
                  "time": timestamp,
                  "fields": {
                      "Total WR1": float(wr1_total),
                      "Total WR2": float(wr2_total)
                            } 
              }
            ]


if(value_style=='current'):

#
# get last result from file
#


  dir_path = os.path.dirname(os.path.realpath(__file__))
  filename = dir_path + "/PV.yaml"

  if(os.path.isfile(filename)): 
    with io.open(filename, 'r') as stream:
      data_loaded = yaml.load(stream)
    prev_result_wr1 = data_loaded['Total_wr1']
    prev_result_wr2 = data_loaded['Total_wr2']
    prev_timestamp = data_loaded['timestamp']
    print("data_loaded: " + str(prev_result_wr1) + ", " + str(prev_result_wr2) + ", " + str(prev_timestamp))
    timestamp_diff = (timestamp - prev_timestamp) / float(3600*1000000000)
    result_diff_wr1 = (float(wr1_total) - float(prev_result_wr1)) * 1000
    result_diff_wr2 = (float(wr2_total) - float(prev_result_wr2)) * 1000
    print ("Since last measurement [h]: " + str(timestamp_diff))
    print ("Since last measurement [s]: " + str(timestamp_diff*3600))
    print ("Total production diff WR1 [W]: " + str(result_diff_wr1))
    print ("Total production diff WR2 [W]: " + str(result_diff_wr2))
    current_wr1 = result_diff_wr1/timestamp_diff
    current_wr2 = result_diff_wr2/timestamp_diff
    print ("Current production WR1 [W]: " + str(current_wr1))
    print ("Current production WR2 [W]: " + str(current_wr2))

  else:    # initialize if there is no prev data
    print("No previous data found")
    timestamp_diff = 3600
    result_diff_wr1 = 0
    result_diff_wr2 = 0
    current_wr1 = 0
    current_wr2 = 0

  data = {'timestamp': timestamp,
         'Total_wr1': float(wr1_total),
         'Total_wr2': float(wr2_total)
          }
   
  with io.open(filename, 'w', encoding='utf8') as outfile:
    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

  json_body = [
                {
                    "measurement": "energy_current",
                    "tags": {
                        "meter": "PV"
                    },
                    "time": timestamp,
                    "fields": {
            		"Current_WR1": float(current_wr1),
                        "Current_WR2": float(current_wr2),
                        "Battery Charge": float(batt_charge)/100
                              } 
                }
            ]

print(json.dumps(json_body, indent=4, sort_keys=True))
client = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_dbname)
client.write_points(json_body)   

