import serial 
import time
import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)

Dist_Total_1 = []
Dist_Total_2 = []

#ser_1 = serial.Serial('/dev/ttyUSB1',115200,timeout=1)
ser_2 = serial.Serial('/dev/ttyUSB0',115200,timeout=1)
#ser.write(0x42)
#ser_1.write(bytes(b'B'))
ser_2.write(bytes(b'B'))
#ser.write(0x57)
#ser_1.write(bytes(b'W'))
ser_2.write(bytes(b'W'))
#ser.write(0x02)
#ser_1.write(bytes(2))
ser_2.write(bytes(2))
#ser.write(0x00)
#ser_1.write(bytes(0))
ser_2.write(bytes(0))
#ser.write(0x00)
#ser_1.write(bytes(0))
ser_2.write(bytes(0))
#ser.write(0x00)
#ser_1.write(bytes(0))
ser_2.write(bytes(0))
#ser.write(0x01)
#ser_1.write(bytes(1))
ser_2.write(bytes(1))
#ser.write(0x06)
#ser_1.write(bytes(6))
ser_2.write(bytes(6))


while(True):
    while(ser_2.in_waiting >= 9):
        if((b'Y'== ser_2.read()) and (b'Y' == ser_2.read())):
        
            #Dist_L_1 = ser_1.read()
            #Dist_H_1 = ser_1.read()
            #Dist_Total_1 = (ord(Dist_H_1)*256)+ord((Dist_L_1))
            
            Dist_L_2 = ser_2.read()
            Dist_H_2 = ser_2.read()
            Dist_Total_2 = (ord(Dist_H_2)*256)+ord((Dist_L_2))
            
            for i in range (0,5):
                #ser_1.read()
                ser_2.read()
                    
        time.sleep(0.0005)
        print (Dist_Total_2)
            #if (Dist_Total > 1):
             #   print ('1')
            #else:
             #   print('0')
