#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Educator Driving Base Program
-----------------------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import struct
from ps4keymapping import EV_KEY, EV_ABS, BTN, AXES

# Initialize the EV3 Brick.
brick = EV3Brick()

# Declare motors 
left_motor = Motor(Port.C)
right_motor = Motor(Port.B)

# Initialize variables. 
# Assuming sticks are in the middle when starting.
left_stick_left = 0
left_stick_forward = 0

right_stick_left = 0
right_stick_foward = 0

right_stick_x = 124
right_stick_y = 124


left_stick_x = 124
left_stick_y = 124

maxPower = 100
minPower = maxPower * -1
maxTurnPower = 80
forward = 0
leftPower = 0
rightPower = 0
# A helper function for converting stick values (0 - 255)
# to more usable numbers (-100 - 100)



# Find the PS3 Gamepad:
# /dev/input/event3 is the usual file handler for the gamepad.
# look at contents of /proc/bus/input/devices if it doesn't work.
# command less /proc/bus/input/devices
infile_path = "/dev/input/event4"

# open file in binary mode
in_file = open(infile_path, "rb")

# Read from the file
# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'    
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)
# stick y top 0 bottom 255, stick x left 0, right 255
while event:
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
    if ev_type == 3 and code == 0:
        left_stick_x = value
    if(ev_type == 3 and code == 1):
        left_stick_y = value
        # print("LY ", left_stick_y)
    if ev_type == 3 and code == 3:
        right_stick_x = value
        # print("RX ", right_stick_x)
    if ev_type == 3 and code == 4:
        right_stick_y = value
    

    # Scale stick positions to -100,100
    if(left_stick_y < 100):
        # stick forward 0-117
        forward = 100  
    elif(left_stick_y > 155):
        # stick back 155-255
        forward = -100
    else:
        forward = 0
    
    if(right_stick_x < 100):
        # stick left 0-117
        turn = 100 - right_stick_x
    elif(right_stick_x > 155):
        # stick right 155-255
        turn = 155 - right_stick_x
    else:
        turn = 0
 
    if(-50 < forward and forward < 50): 
        # turn no run
        if(turn > 50):
            #   turn left spin left forward
            leftPower = 0
            rightPower = maxTurnPower      
        elif turn< (-50):
            #   turn righ spin right forward
            leftPower = maxTurnPower *  - 1
            rightPower = 0     
        else:
            leftPower = 0
            rightPower = 0
    elif (forward > 50):
        # run and turn
        
        if(turn > 50):
            #   turn left slow down left motor
            leftPower = forward * 0.3
            rightPower = forward
        elif turn< (-50):
            #   turn right slow down right motor
            rightPower = forward * 0.3
            leftPower = forward
            # print("LP ", leftPower, " RP ", rightPower)  
        else:
            rightPower = forward
            leftPower = forward
    elif (forward < -50):
        if(turn > 20):
            #   turn right slow down right motor
            leftPower = forward * 0.3
            rightPower = forward
        elif turn < (-20):
            #   turn left slow down left motor
            rightPower = forward * 0.3      
            leftPower = forward
            
        else:
            rightPower = forward
            leftPower = forward
    else:
            rightPower = 0
            leftPower = 0
    # print("LY ", left_stick_y, " RX ", right_stick_x, "  forward: ", forward, " turn: ", turn," R ",rightPower," L ",leftPower)

    # wait(500)

    # Set motor voltages. If we're steering left, the left motor
    # must run backwards so it has a -left component
    # It has a forward component for going forward too. 
    print("LP ", leftPower, " RP ", rightPower)
    left_motor.dc(leftPower)
    right_motor.dc(rightPower)

    # Finally, read another event
    event = in_file.read(EVENT_SIZE)

in_file.close()