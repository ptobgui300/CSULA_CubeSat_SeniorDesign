#just a script to test connection to influxdb and generating random data
from influxdb import InfluxDBClient
import random

try:
    dbClient = InfluxDBClient('192.168.43.128', 8086, 'root', 'root', 'test')
    while True:
        print("got to here")
        speed = random.uniform(0,101)
        events = [{"measurement": "speed",
                  
                  "fields": {
                      "speed": speed
                    }
                }]
        print("got to 2")
        dbClient.write_points(events)
        print("got to 3")
except:
    print('something went wrong')
