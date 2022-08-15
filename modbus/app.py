#
# This is a python3 script
#

#
# pip install modbus_tk flask
#
# OPERATION
# sudo nano /etc/systemd/system/my_flask.service

### [Unit]
### Description=My Flask server for mosbus data
### After=network.target
### 
### [Service]
### User=pi
### WorkingDirectory=/home/pi/read-powerconsumption/modbus
### ExecStart=/home/pi/.local/bin/flask run --host 0.0.0.0
### Restart=always
### Environment=FLASK_CONFIG=development
### 
### 
### [Install]
### WantedBy=multi-user.target

# sudo systemctl status my_flask
# sudo systemctl status my_flask
# sudo systemctl status my_flask
#


#https://realpython.com/api-integration-in-python/#flask

from flask import Flask, request, jsonify

import socket
import pytz
from datetime import datetime

rest_server = Flask(__name__)

pow2_48 = 281474976710656
pow2_32 = 4294967296
pow2_16 = 65536

def cli_help():
  print("Usage: read-modbus-server.py !needs update")
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
    return result

def fourToupleRegister2int(input_t):
  result = input_t[0] * pow2_48 + input_t[1] * pow2_32 + input_t[2] * pow2_16 + input_t[3]
  return result	

tz_Berlin = pytz.timezone('Europe/Berlin') 
	
#print("WR1:  " + "{0:.2f}".format(wr1_total))
#print("WR2:  " + "{0:.2f}".format(wr2_total))
#print("SOC:  " + "{0:.0f}".format(batt_charge))

s_help = "Usage:\n/soc: State of Charge\n/total_production: Total solar power"

@rest_server.get("/")
def get_root():
   return(s_help)

@rest_server.get("/help")
def get_help():
  return(s_help)

@rest_server.get("/soc")
def get_SOC():
  output93 = read_modbus("192.168.2.93", 30845, 2)
  batt_charge = float(output93[1])
  timestamp = datetime.now(tz_Berlin)
  json_body = [
              { "time": 
                {
                    "year": timestamp.year,
                    "month": timestamp.month,
                    "day": timestamp.day,
                    "hour": timestamp.hour,
                    "minutes": timestamp.minute,
                    "seconds": timestamp.second,
                },
                "Battery Charge": batt_charge
              }
            ]
  return(jsonify(json_body)) 

@rest_server.get("/total_production")
def get_Current_Production():
  output91 = read_modbus("192.168.2.91", 30513, 4)
  output92 = read_modbus("192.168.2.92", 30513, 4)
  wr1_total = float(fourToupleRegister2int(output91))/1000
  wr2_total = float(fourToupleRegister2int(output92))/1000
  timestamp = datetime.now(tz_Berlin)
  json_body = [
              { "time": 
                {
                    "year": timestamp.year,
                    "month": timestamp.month,
                    "day": timestamp.day,
                    "hour": timestamp.hour,
                    "minutes": timestamp.minute,
                    "seconds": timestamp.second,
                },
                "WR1": wr1_total,
                "WR2": wr2_total
              }
            ]
  return(jsonify(json_body)) 


