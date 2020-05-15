
from os import sys, path

import time
import math
import argparse


#--------------------------------------------------
#-------------- FUNCTIONS  
#--------------------------------------------------    


#Goal of this navigation is to have CubeSat Rotate a degree/ angle; with the goal of 
# having the target aligned in its center before thrusting toward target.

# ---HEADING CONTROLS
# By knowing how long SimPlat takes to rotate a full 360 we can computer the amount of
# time it takes to move N degrees. 
# Now that we have time it takes to rotate a certain degree/angle, we can use this to send a 
# rotate command for X amount of seconds before sending counter thrusting to stop rotation .
# This will line us up with the target in the center of our screen. 

# XYZ -> Angle-> Rotate(angle) ->computeRotateTime(angel) ->startRotate(seconds )


def marker_position_to_angle(x, y, z):
    
    angle_x = math.degrees(math.atan2(x,z))
    angle_y = math.degrees(math.atan2(y,z))
    print("the angle betwen x : ",x," and z :",z," is :",angle_x)
    print("the angle betwen y :",y," and z :",z," is :",angle_y)
    
    return (angle_x, angle_y)
    

def calcDegreeRate(degree,full360inSeconds):
    # if we know rate it takes for SimPlat to complete a complete 360 degree rotation, 
    # we can calcute what  rate it takes to complete a desired angle
    # example here is if SimPlat were to take 4 seconds to rotate a complete 360

    seconds = full360inSeconds/360
    secondsToRotateAngle = seconds*degree
    print("it will take ",secondsToRotateAngle," seconds to rotate ",degree," degrees")
    return secondsToRotateAngle

   
def headerControl(degree):
    return thrustCommand,seconds


def rotate_thruster(thrustCommand,seconds):

    return delayCommand


def sendDelayedCommand(delayCommand,secondsToThrust):

    rotateClockWise = "rotateClockWise"
    rotateCounterClockWise = "rotateCounterClockWise"
    thrustForward = "thrustForward"
    thrustReverse = "thrustReverse"

    print("send thruster command to SimPlat")



distanceGoal        = 50.0
full360inSeconds = 4.0
loop =True

while loop is True:                
    
    marker_found = True
    # (x,y, z) add test values
    # marker_found, x, y, z = aruco_tracker.track(loop=False) # Note : XYZ  are all in cm
    testValues = [-10,5,20]
    x = testValues[0]
    y= testValues[1]
    z = testValues[2]

    rotateDirection =""

    if marker_found:
        #rotateCCW()
        #degree = marker_position_to_angle(x,y,z)
        #rate = headerControl(degree)
        #delay_command = rotate_thruster(rate))
        #sendDelayedCommand(rate)    # inner loop that takes delay(sends 2 commands, 1 before delay and 1 after)
        # = ^loop delay()
        #   ^if checkthreshold(x,y,z) == false
        #       ^sendStop()
        #=  ^else continue
        # = send last command
        

        angle_x, angle_y    = marker_position_to_angle(x, y, z)
        if angle_x >0:
            rotateDirection = "rotateClockwise "
            print(rotateDirection)
        if angle_x < 0:
            rotateDirection = "rotateCounterClock"
            print(rotateDirection)


        secondsToRotate  = calcDegreeRate(angle_x,full360inSeconds)

        sendDelayedCommand(rotateDirection,secondsToRotate)

        loop = False

