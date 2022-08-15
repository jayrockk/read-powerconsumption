# read-powerconsumption
Collection of tools to read utiliy and photovoltaics consumption and production data. Write to display, influxdb, or http client.

I wrote these scripts to fit my personal requirements, and I hope they are useful for others as code examples or inspiration. Aplogies for the English/German mish-mash.

All runs perfectily fine on a first-gen RaspberryPi. 

#1. USB-Head/USB_read.py
Reads the power meter provided by my local utiliy. Uses the IR Head specifie by https:www.volkszahler.org. The meter brand and type is Easymeter Q3M, which does not seem to be available anymore. I'm using the INFO-DSS interface. If you have a different meter, the SML message detection my need some adjustment.

The script outputs total energy figures to the console, and writes to influxdb

#2. modubs/read-modbus-python3.py
Utilzing modbus, read total production power from SMA Sunny Boy Inverters, and the State of Charge of SMA Sunny Island. Console output and optional writing to influxdb. If you have different SMA boxes, the message addresses may need adjustment. (And obviously you need to change the IP addresses.)

#3 modbus/app.py
A FLASk application (https://flask.palletsprojects.com/) that delivers total power production and SoC from the SMA system in json format to an https client. 
