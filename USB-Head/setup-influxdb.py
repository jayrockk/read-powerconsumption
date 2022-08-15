#pip install requests OR python -m pip install requests
from influxdb import InfluxDBClient


host = "192.168.0.104"
port = "8086"
user = "root"
password = "root"
dbname = "energy"
dbuser = "energy"
dbuser_password = "energypassword"

client = InfluxDBClient(host, port, user, password, dbname)

#
# Uncomment to drop database before creating a new one
#
#client.drop_database(dbname)

print("Create database " + dbname + " on " + host)
client.create_database(dbname)

print("Switch user: " + dbuser)
client.switch_user(dbuser, dbuser_password)
