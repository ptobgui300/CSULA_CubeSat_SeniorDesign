from os import sys, path
import time
import math
import argparse
# --------------------------------------------------
# -------------- FUNCTIONS
# --------------------------------------------------
# Goal of this navigation is to have CubeSat Rotate a degree/ angle; with the goal of
# having the target aligned in its center before thrusting toward target.
# ---HEADING CONTROLS
# By knowing how long SimPlat takes to rotate a full 360 we can computer the amount of
# time it takes to move N degrees.
# Now that we have time it takes to rotate a certain degree/angle, we can use this to send a
# rotate command for X amount of seconds before sending counter thrusting to stop rotation .
# This will line us up with the target in the center of our screen.
# XYZ -> Angle-> Rotate(angle) ->computeRotateTime(angel) ->startRotate(seconds )

thrustDic = {'Stop': ['0000 0000'],
             'Left': ['0110 0000'], 
             'Right': ['0000 0110'], 
             'Forward': ['0001 1000'], 
             'Backward': ['1000 0001'], 
             'UpperRightDiagonal': ['0001 1110'], 
             'UpperLeftDiagonal' : ['0111 1000'], 
             'BottomRightDiagonal' : ['1000 0111'], 
             'CounterClockWise' : ['0101 0101'], 
             'ClockWise' : ['1010 1010']}

distanceGoal = 10.0
full360inSeconds = 4.0
loop = True

testValues = [11, 5, 20]     
x = testValues[0]
y = testValues[1]
z = testValues[2]

def marker_position_to_angle(x, y, z):
    angle_x = math.degrees(math.atan2(x, z))
    angle_y = math.degrees(math.atan2(y, z))
    # print("the angle betwen x : ", x, " and z :", z, " is :", angle_x)
    # print("the angle betwen y :", y, " and z :", z, " is :", angle_y)
    return (angle_x, angle_y)

def calcDegreeRate(degree, full360inSeconds):
# if we know rate it takes for SimPlat to complete a complete 360 degree rotation,
# we can calcute what  rate it takes to complete a desired angle
# example here is if SimPlat were to take 4 seconds to rotate a complete 360
    seconds = full360inSeconds / 360
    secondsToRotateAngle = seconds * degree
    # print("it will take ", secondsToRotateAngle, " seconds to rotate ", degree, " degrees")
    return secondsToRotateAngle

def headerControl(degree):
    # if the degree is negative, that means the target is to the left of CubeSat so a clockwise rotation is neccessary,
    # else if the degree is positive, the target is to the right of CubeSat so a counter-clockwise rotation is needed
    # Jonathan's note: im currently leaving thrustCommand as a string variable because I'm not sure what type we want to be output from here
    if degree < 0:
        thrustCommand = 'ClockWise'
    elif degree > 0:
        thrustCommand = 'CounterClockWise'
    else:
        print("Stop")
    print(thrustCommand)
    seconds = calcDegreeRate(degree, full360inSeconds)
    print(seconds)
    return thrustCommand #, seconds

def velocityControl(dist):
    if dist > distanceGoal:
        delayCommand = 'Forward'            
    if dist <= distanceGoal:
        delayCommand = 'Stop'
      
    return delayCommand
    # sendDelayedCommand(delayCommand)
    
def rotate_thruster(thrustCommand, seconds):
    return delayCommand

def opposite_thrust(thrustCommand):         # thrustCommand is a string 
    return

# Check if binary has a space between the 0's
def sendDelayedCommand(delayCommand):
    print("send thruster command to SimPlat")
    thruster = ['0000 0000']
    # Basic Motions
    
    return thrustDic[delayCommand]
    """
    if delayCommand == 'Left':
        thruster = ['0110 0000']
    elif delayCommand == 'Right':
        thruster = ['0000 0110']
    elif delayCommand == 'Forward':
        thruster = ['0001 1000']
    elif delayCommand == 'Backward':
        thruster = ['1000 0001']
    # DiagonalMotions
    elif delayCommand == 'UpperRightDiagonal':
        thruster = ['0001 1110']
    elif delayCommand == 'UpperLeftDiagonal':
        thruster = ['0111 1000']
    elif delayCommand == 'BottomLeftDiagonal':
        thruster = ['1110 0001']
    elif delayCommand == 'BottomRightDiagonal':
        thruster = ['1000 0111']
    # Rotation
    elif delayCommand == 'CounterClockWise':
        thruster = ['0101 0101']
    elif delayCommand == 'ClockWise':
        thruster = ['1010 1010']
    print('Nav Command:', delayCommand)
    print('Thruster Command:', thruster)
    return thruster
    """
def test(test_vals, thrusterCommand):
    if thrusterCommand == ['0101 0101']:
        testValues[0] -= 1
    elif thrusterCommand == ['1010 1010']:
        testValues[0] += 1
    elif thrusterCommand == ['0001 1000']:
        testValues[2] -= 2
    elif thrusterCommand == ['0000 0000']:
        print(f'distance: {testValues[2]}')
    else:
        print("NOT A COMMAND")
    
while loop is True:
    marker_found = True
    # (x,y, z) add test values
    # marker_found, x, y, z = aruco_tracker.track(loop=False) # Note : XYZ  are all in cm
    x = testValues[0]
    y = testValues[1]
    z = testValues[2]
    
    
    
    if marker_found:
        angle_x, angle_y = marker_position_to_angle(x, y, z)
        secondsToRotate = calcDegreeRate(angle_x, full360inSeconds)
        
        if angle_x:
            delayed = headerControl(angle_x)
        else:
            delayed = velocityControl(z)
        
        command = sendDelayedCommand(delayed)
        print(f'command: {command}')
        
        test(testValues, command)
    time.sleep(1)
        # loop = False
    # rotateCCW()
    # degree = marker_position_to_angle(x,y,z)
    # rate = headerControl(degree)
    # delay_command = rotate_thruster(rate))
    # sendDelayedCommand(rate)    # inner loop that takes delay(sends 2 commands, 1 before delay and 1 after)
    # = ^loop delay()
    #   ^if checkthreshold(x,y,z) == false
    #       ^sendStop()
    # =  ^else continue
    # = send last command
     