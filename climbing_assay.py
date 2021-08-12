## Main file for the climbing assay
## Written August 5, 2021 by Adam Spierer
## Adapted from an earlier script written on July 7, 2015 by Adam Spierer
##
## The purpose of this script is to run the data generation step of the Drosophila climbing assay.
##   In brief, the program will record videos of flies climbing up vials that are timed with the
##   moment of the drop. Videos and images are named with user-defined experimental details
##   (genotype, sex, etc).
##
##   These data are recorded using a Raspberry Pi microcomputer with several of the GPIO
##   pins. Pins correspond with signal processing through an MCP3008 chip (analog-digital converter),
##   powering a light sensor, and controlling colored LED lights.
##
##   The output of this program can be ported to the FreeClimber package for rapid analysis.
##
##   BEFORE RUNNING!!! Make sure device.py script contains the correct user-defined
##   variables in the `define_variables` function. Otherwise, the program will not match the
##   intended design.
##########################################################################
## Loading the climbing_rig object with the main functions and variables
from device import climbing_rig
import RPi.GPIO as GPIO

##########################################################################
## Create an instance for the climbing_rig class in device.py
device = climbing_rig()

def main():
    '''Main script that loops through the conditions that need to be recorded'''
    ## Loop through genotypes
    for i in range(len(device.genotypes)):
        ## Create directory for genotype
        device.dir_geno = device.dir_time + device.genotypes[i] +'/'
        device.create_directory(device.dir_geno)
        
        ## Loop through sexes
        for j in range(len(device.sex)):
            ## Print statement to acknowledge a new genotype, sex, or genotype-sex combination
            print('#' * 25)
            print(10 * '#' + '  ' + device.genotypes[i])
            print(10 * '#' + '  ' + device.sex[j])
            print('#' * 25 + '\n')
            
            ## Create directory for sex
            device.dir_sex = device.dir_geno + device.sex[j] +'/'
            device.create_directory(device.dir_sex)
            
            ## Iterate through the replicates
            for rep in range(1,device.replicate_number + 1):
                device.execute_capture(device.genotypes[i], device.sex[j], rep, device.replicate_number)
            
            ## Check-in following the completion of a sex-genotype combination
            ## Program will do single replicates, recalibrate the detector, or move onto the next sex-genotype combination
            while True:
                device.checkin(device.genotypes[i],device.sex[j], rep)
                break
                
    print('Recording location:', device.dir_working)
    return

## Work through the main program
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Program halted due to keyboard interrupt @',device.file_root)
    finally:
        print('END')
        