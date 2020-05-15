import time
import board
import busio
import adafruit_lsm9ds1
import json
from influxdb import InfluxDBClient

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

fo = open("foo.txt", "w")
data = {}
data['Acceleration'] = []
data['Magnetometer'] = []
data['Gyroscope'] = []
data['Temperature'] = []

try:
    #change ip to ip of the machine InfluxDB is running on and 'test' to the name of database being used
    dbClient = InfluxDBClient('192.168.43.128', 8086, 'root', 'root', 'test')
    i=0
    #dbClient.ping()
    print('Starting data transfer...')
    while True:
        
        
        #print('its at the start of while', i)
        #i+=1
        accel_x, accel_y, accel_z = sensor.acceleration
        mag_x, mag_y, mag_z = sensor.magnetic
        gyro_x, gyro_y, gyro_z = sensor.gyro
        temp = sensor.temperature
        #print(accel_x)
        
        events = [{"measurement": "temp",
                   
                   "fields": {
                        "temperature": temp
                    }
                   },
                  {"measurement": "acceleration",
                       
                       "fields": {
                           "accel_x": accel_x,
                           "accel_y": accel_y,
                           "accel_z": accel_z
                           }
                    }, {"measurement": "magnetic",
                        
                        "fields": {
                            "mag_x": mag_x,
                            "mag_y": mag_y,
                            "mag_z": mag_z
                            }
                        }, {"measurement": "gyroscope",
                            
                            "fields": {
                                "gyro_x": gyro_x,
                                "gyro_y": gyro_y,
                                "gyro_z": gyro_z
                                }
                            
                            }]
        #print('before write')
        dbClient.write_points(events)
except:
        print("something went wrong")