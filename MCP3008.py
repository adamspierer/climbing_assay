## Function and variable file for the climbing assay
## Written August 5, 2021 by Adam Spierer
## Adapted from an earlier script written on July 7, 2015 by Adam Spierer
##
## --> Make sure to modify the `define_variables` function on lines 36 - 59
##     before running the main climbing_assay.py script.
##
## NOTE: Code sourced and modified from: https://tutorials-raspberrypi.com/mcp3008-read-out-analog-signals-on-the-raspberry-pi/
##########################################################################
## Import modules
from spidev import SpiDev

##########################################################################
## Define analog-digital converter (ADC) object
class MCP3008:
    def __init__(self, bus = 0, device = 0):
        '''Initialize and run the ADC converter'''
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000 # 1MHz
 
    def open(self):
        '''Open port'''
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz
    
    def read(self, channel = 0):
        '''Read channel'''
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
            
    def close(self):
        '''Close port'''
        self.spi.close()