## Function and variable file for the climbing assay
## Written August 5, 2021 by Adam Spierer
## Adapted from an earlier script written on July 7, 2015 by Adam Spierer
##
## --> Make sure to modify the `define_variables` function on lines 36 - 59
##     before running the main climbing_assay.py script.
##
## NOTE: Code sourced and modified from: https://tutorials-raspberrypi.com/mcp3008-read-out-analog-signals-on-the-raspberry-pi/
##
##########################################################################
## Import modules
from MCP3008 import MCP3008
from time import sleep

##########################################################################
## Define variables
channel = 0 # Change if using a different channel

##########################################################################
## Initialize the MCP3008 OBJECT
adc = MCP3008()

##########################################################################
## Run the ADC converter
while True:
    ## Read the analog-digital converter
    value = adc.read(channel)

    ## Print voltage
    print("Applied voltage: %.4f" % (value))# / 1023.0 * 3.3) ) # Uncomment for precise voltage instead of units read in
    sleep(.1) # A delay is nice so the output doesn't overwhelm the terminal