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
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize variables. 
# Assuming sticks are in the middle when starting.
right_stick_x = 124
right_stick_y = 124

left_stick_x = 124
left_stick_y = 124

# A helper function for converting stick values (0 - 255)
# to more usable numbers (-100 - 100)
def scale(val, src, dst, zero_offset_min=-0.0, zero_offset_max=0.0):
    """
    แปลงค่า val จากช่วง src ไปยังช่วง dst และตัดค่าเล็กๆ ให้เป็น 0 ถ้าอยู่ในช่วง zero offset

    val: ค่าที่จะถูกแปลง
    src: tuple เช่น (0, 255)
    dst: tuple เช่น (-100, 100)
    zero_offset_min: ค่าน้อยสุดที่ถือว่าเป็น 0
    zero_offset_max: ค่าสูงสุดที่ถือว่าเป็น 0

    เช่น scale(128, (0, 255), (-100, 100), -3, 3) -> 0
    """
    scaled = (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

    if zero_offset_min <= scaled <= zero_offset_max:
        return 0.0
    return scaled


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

while event:
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
    if ev_type == 3 and code == 0:
        left_stick_x = value
    if(ev_type == 3 and code == 1):
        left_stick_y = value
    if ev_type == 3 and code == 3:
        right_stick_x = value
    if ev_type == 3 and code == 4:
        right_stick_y = value
    

    # Scale stick positions to -100,100
    forward = scale(left_stick_y, (0,255), (100,-100),-3,3)
    left = scale(right_stick_x, (0,255), (100,-100),-3,3)

    # Set motor voltages. If we're steering left, the left motor
    # must run backwards so it has a -left component
    # It has a forward component for going forward too. 
    left_motor.dc(forward - left)
    right_motor.dc(forward + left)

    # Finally, read another event
    event = in_file.read(EVENT_SIZE)

in_file.close()