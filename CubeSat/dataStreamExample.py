#this script should be on CubeSat and both the CubeSat and the machine hosting InfluxDB must be on the same network
#Note: this script is not exactly the same as the one CubeSat as of 10/31. The one on CubeSat streams the proper data to InfluxDB

from influxdb import InfluxDBClient
import random
import json
from datetime import datetime


try:
    #change localhost to the ip of the machine that is hosting influx database and change test to name of database being used
    ip = "localhost"
    database = "test"
    print('Attempting to connect...')
    dbClient = InfluxDBClient('localhost', 8086, 'root', 'root', 'test')
    print('Connection Successful')
    print(dbClient.ping())
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")
    print('Writing data to database...')

    while True:
        #Sample of how to write the data that is being sent to InfluxDB
        accel_x = random.uniform(-10,10)
        accel_y = random.uniform(-10, 10)
        accel_z = random.uniform(-10, 10)
        gyro_x = random.uniform(-10,10)
        gyro_y = random.uniform(-10, 10)
        gyro_z = random.uniform(-10, 10)
        mag_x = random.uniform(-10,10)
        mag_y = random.uniform(-10, 10)
        mag_z = random.uniform(-10, 10)
        temp = random.uniform(-50,50)
        events = [{"measurement": "CubeSat",

                   "fields": {
                       "accel_x": accel_x,
                       "accel_y": accel_y,
                       "accel_z": accel_z,
                       "mag_x": mag_x,
                       "mag_y": mag_y,
                       "mag_z": mag_z,
                       "gyro_x": gyro_x,
                       "gyro_y": gyro_y,
                       "gyro_z": gyro_z,
                       "temperature": temp,
                       "timeStamp": currentTime
                   }

       }]
        #print('test')
        dbClient.write_points(events)
        #print('woo')
except:
    print("Something went wrong.")
    #print('inserted data')
    #time.sleep()

#with open('data.txt') as json_file:
#    data = json.load(json_file)
