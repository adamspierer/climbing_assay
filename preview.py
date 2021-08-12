## Function and variable file for the climbing assay
## Written August 5, 2021 by Adam Spierer
## Adapted from an earlier script written on July 7, 2015 by Adam Spierer
##
## --> Make sure to modify the `define_variables` function on lines 36 - 59
##     before running the main climbing_assay.py script.
##
## This script is not essential or called in the climbing_assay script.
##    It is useful for getting a visual on the rig when setting up the assay.
##########################################################################
## Import modules
import time
import spidev
import picamera
import RPi.GPIO as GPIO

##########################################################################
## Define variable
move_on = False

##########################################################################
## Define functions
def previewer():
    ''''''
    delay_time = 0.00001
    capture = delay_time
    while capture != 0:
        camera.resolution = (1280, 960)
        camera.rotation = 180
        camera.start_preview()  
        time.sleep(int(capture))
        camera.stop_preview()
        capture = input("Live view for how many seconds??:  ")
        if capture == '' or capture == '0':
            break
        
def print_opener():
    '''Prints opening statements when the program is first run'''
    print("\n\nWelcome to preview.py!")
    print("  - The goal of this script is to view the Raspberry Pi camera image...")
    print("  - Ensure image is framed correctly and there is no 'banding' pattern...")
    print("  - If banding, hold the power icon on the lightboard to adjust until gone...")
    print("\nTo use:")
    print("  - Enter the number of seconds to view for...")
    print("  - When you are finished, press <enter> to exit the program...")
    print("\n~~Happy viewing~~\n\n")
    return

##########################################################################
## Running the camera
with picamera.PiCamera() as camera:
    while move_on == False:
        move_on = previewer()