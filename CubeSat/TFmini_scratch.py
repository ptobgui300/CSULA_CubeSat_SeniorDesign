import serial 
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

Dist_Total_3 = []

# check /dev for devices plugged in
# currently, we're using the USB port
addr1 = '/dev/ttyUSB0'
ser_3 = serial.Serial(addr1,115200)

#ser.write(0x42)
ser_3.write(bytes(b'B'))
#ser.write(0x57)
ser_3.write(bytes(b'W'))
#ser.write(0x02)
ser_3.write(bytes(2))
#ser.write(0x00)
ser_3.write(bytes(0))
#ser.write(0x00)
ser_3.write(bytes(0))
#ser.write(0x00)
ser_3.write(bytes(0))
#ser.write(0x01)
ser_3.write(bytes(1))
#ser.write(0x06)
ser_3.write(bytes(6))


while(True):
    while(ser_3.in_waiting >= 9):
        if((b'Y'== ser_3.read()) and (b'Y' == ser_3.read())):
        
            Dist_L_3 = ser_3.read()
            Dist_H_3 = ser_3.read()
            Dist_Total_3 = (ord(Dist_H_3)*256)+ord((Dist_L_3))
            
            for i in range (0,5):
                ser_3.read()
                    
        #time.sleep(0.5)
        print (Dist_Total_3)
            #if (Dist_Total > 1):
             #   print ('1')
            #else:
             #   print('0')
