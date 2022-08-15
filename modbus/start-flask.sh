#/bin/sh
cd /home/pi/read-powerconsumption/modbus
export FLASK_APP=/home/pi/read-powerconsumption/modbus/rest-server.py
export FLASK_ENV=development
flask run --host 0.0.0.0
