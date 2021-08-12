## Function and variable file for the climbing assay
## Written August 5, 2021 by Adam Spierer
## Adapted from an earlier script written on July 7, 2015 by Adam Spierer
##
## --> Make sure to modify the `define_variables` function on lines 36 - 59
##     before running the main climbing_assay.py script.
##########################################################################
## Import modules
import os
from time import sleep,ctime
import picamera
import numpy as np
import RPi.GPIO as GPIO
from MCP3008 import MCP3008

##########################################################################
## Load climbing_rig object with nested functions
class climbing_rig:
    '''Aggregated functions and variables used to run the climbing rig hardware and software'''
    def __init__(self):
        ## Print opening lines
        self.print_open()
        
        ## Initialize important variables and pins
        self.define_variables()
        self.setup_board()
        self.genotypes = self.create_genotype_list()
        
        ## Calibrate the light sensor
        self.triggerThreshold = self.autocalibrator()
        
        ## Initialize directories
        self.setup_directories()
        return
        
    def define_variables(self):
        ## Basic options - Experimental conditions
        self.nuc = ['1', '2']
        self.mito = ['w1118']
        self.extra_genotypes = [] # Add extra genotypes from past experiments (eg. si1_7744)
        self.delete_genotypes = [] # Update with genotypes to delete from the list (those not present)
        self.sex = ['m']

        ## Basic options - Recording parameters
        self.dir_home = '/home/pi/Desktop/deficiency_screen/'
        self.capture_time = 1     # Seconds to record video (5 ideally)
        self.wait_time = 1        # Seconds between knockdowns (10 ideally)
        self.replicate_number = 2 # Number of replicate knockdowns

        ## Advanced options - General
        self.trigger_sensitivity = 10 ## Set to 0.6 if testing to bypass the light sensor
        self.n_samples_for_trigger_calibration = 5

        ## Advanced options - GPIO pins
        self.channel = 0 # Only play with this if you know what you are doing...corresponds with the channel on the MCP3008 chip to read the photoresistor
        self.red = 11
        self.yellow = 13
        self.green = 15
        return
    
    ## Setting board mode and LED pin assignments
    def setup_board(self):
        '''Setting up the board mode and assigning pins to LEDs'''    
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.yellow, GPIO.OUT)
        GPIO.setup(self.red, GPIO.OUT)

        ## Setting pin brightness
        GPIO.output(self.green, GPIO.LOW)
        GPIO.output(self.yellow, GPIO.HIGH)
        GPIO.output(self.red, GPIO.LOW)

        ## Set up ADC
        self.adc = MCP3008()
        return
    
    ## Create parent directory with user input
    def setup_directories(self): 
        '''Setting up the directories for the file to save'''
        ## Establish Global Variables
        print('  Recording variables: %s second videos and waiting %s seconds between knockdowns' % (self.capture_time, self.wait_time))
        print('Currently in folder: ', self.dir_home)
        print(40 * '-')

        ## User establishes the working directory
        print('List of directories within home directory: ')
        print('  -1 :: New')
        self.dir_list = sorted([item for item in os.listdir(self.dir_home) if ~item.startswith('.') or ~item.endswith('.py')])
        for i in range(len(self.dir_list)): # Listing the different folders in home directory
            print('   ' + str(i) + ' :: ' + self.dir_list[i])
        
        ## Allows user to select a project or batch to add longitudinal data to
        project = int(input('Select a project number or add a new one: ')) #Prompt user for folder number
        if project == -1: # Checks to see if a new folder is being created
            while True:
                new_project = input('Enter a new folder name: ')
                self.dir_working = str(self.dir_home+new_project + '/')
                try:
                    os.mkdir(self.dir_working)
                    break
                except:
                    print('Folder already exists. Try again.')
        else: #finds the folder to add to
            self.dir_working = str(self.dir_home + self.dir_list[project] + '/')
        print('Working directory: ', self.dir_working)
        print(40 * '-')
        
        ## Check to see if folder name is in use, prompt user if so
        while True:
            try:
                self.time_point = str(input('What day is this (ex. 01)?? '))
                self.dir_time = self.dir_working + 'Day_' + str(self.time_point) + '/'
                os.mkdir(self.dir_time)
                print(40 * '-' + '\n')
                break
            except:
                print('Folder name is taken. Try again')                
        
        ## Preview command
        move_on = False
        while move_on == False:
            move_on = self.previewer()
        
        ## Turn yellow light off
        GPIO.output(self.yellow, GPIO.LOW)
        return
    
    ## Concatenating mito and nuclear names
    def create_genotype_list(self):
        '''Creates a list of genotypes to process throughout the experiment.'''
        genotype = []
        for n in self.nuc:
            for m in self.mito:
            	for s in self.sex:
	                genotype.append(m + '_' + n + '_' + s)
        for _extra in self.extra_genotypes:
            genotype.append(_extra)
        for _delete in self.delete_genotypes:
            genotype.remove(_delete)
        print('Evaluating the following genotype x sex combinations:', genotype)
        return(genotype)

    ## Calculates the mean of n-subsequent light sensor readings
    def calibrate_extremes(self):
        '''Sub-function to calculate the mean of `n` samples gathered ~0.1sec apart'''
        value_list = []
        for i in range(self.n_samples_for_trigger_calibration):
            sleep(0.1)
            sensor_value = self.adc.read(self.channel)
            print('  ', sensor_value)
            value_list.append(sensor_value)
        avg = np.mean(value_list)
        return(avg)
    
    ## Autocalibrate the phototrigger
    def autocalibrator(self):
        '''Autocalibrates the phototrigger by having the user raise and lower the rig.'''
        avgHigh=False
        GPIO.output(self.yellow,GPIO.HIGH)
        
        ## Calculate average lowered value
        print('Calibrating light sensor...')
        avgLow = self.calibrate_extremes()
        
        ## Calculate the average raised value
        print('--> Raise climbing rig')
        #print('    ...values will print ever 1/2 second until rig is raised...')
        while avgHigh == False:
            sensor_value = self.adc.read(self.channel)
            #sleep(0.2)
            #print('Sensor value: %s  | avgLow: %s' % (sensor_value,avgLow)) # For debugging an overly sensitive system
            if (self.adc.read(self.channel) > (avgLow + 1) * self.trigger_sensitivity) & (self.adc.read(self.channel) > (avgLow + 1) * self.trigger_sensitivity): # Raised sensor value needs to be at least 150% of what the average low is
                print('Begin counting high threshold...')
                avgHigh = self.calibrate_extremes()
        
        ## Calculate the threshold to trigger
        print('--> Lower climbing rig')
        thresh = np.mean([avgHigh,avgLow])
        print('Low = %s | Threshold = %s | High = %s' % (avgLow, str(round(thresh,1)), avgHigh))
        print('_' * 40)
        
        while self.adc.read(self.channel) < thresh:
            print('Autoclaibration complete!')
            break
        return thresh  

    ## View the camera
    def previewer(self):
        '''Allows the user to preview what the camera sees.'''
        with picamera.PiCamera() as camera:
            delay_time = 0.00001
            capture = delay_time
            while capture != 0:
                GPIO.output(self.red, GPIO.HIGH)
                GPIO.output(self.yellow,GPIO.LOW)
                camera.resolution = (1280, 960)
                camera.rotation = 180
                camera.preview_fullscreen = False
                camera.preview_window = (640, 550, 640, 480)
                camera.start_preview()  
                sleep(int(capture))
                camera.stop_preview()
                GPIO.output(self.yellow,GPIO.HIGH)
                GPIO.output(self.red,GPIO.LOW)
                capture = input('How long do you want to live view (sec)??:  ')
                if capture == '' or capture == '0':
                    capture = 0
                    GPIO.output(self.yellow,GPIO.HIGH)
                    GPIO.output(self.red,GPIO.LOW)
        print(25 * '_')
        
    ## Visual aid during assay
    def blink(self,pin):
        '''Makes an LED flash'''
        GPIO.output(pin, GPIO.HIGH)
        sleep(0.03)
        GPIO.output(pin, GPIO.LOW)
        sleep(0.03)
        return
    
    ## Record the video
    def time_to_capture(self,file_root):
        '''Creates a video recording with the specified parameters and displays feed while recording.'''
        with picamera.PiCamera() as camera:
            ## Change lights
            GPIO.output(self.yellow, GPIO.LOW)
            GPIO.output(self.red, GPIO.HIGH)
            
            ## Set up camera
            camera.resolution = (1280, 960)
            camera.hflip = True
            camera.vflip = True
            
            ## Capture video with active preview
            camera.start_recording(self.dir_active + self.file_root + '.h264')
            camera.preview_fullscreen=False
            camera.preview_window=(640, 550, 640, 480)
            camera.start_preview()  
            camera.wait_recording(self.capture_time)
            camera.stop_recording()
            camera.stop_preview()
            print('Video captured! @ %s' % (ctime()[0:19]))
            
            ## Capture image
            camera.capture(self.dir_active + self.file_root + '.jpg')
            print('Image %s acquired' % self.file_root)
            
            ## Switch light state and rest
            GPIO.output(self.yellow, GPIO.HIGH)
            GPIO.output(self.red, GPIO.LOW)
            sleep(self.wait_time)
            GPIO.output(self.yellow, GPIO.LOW)
            print(25*'_')
            return

    ## Trigger the camera
    def trigger(self):
        '''Triggering mechanism for when the climbing rig slides up and comes back down'''
        trigger0, trigger1, record = False, False, False
        cycle = 0
        while record == False:
            ldr_value = self.adc.read(self.channel)
            if ldr_value > self.triggerThreshold and ldr_value > self.triggerThreshold:
                if cycle == 0: 
                    print('  Armed.......[sensor = %s | threshold = %s]' % (ldr_value, self.triggerThreshold))
                    cycle = 1
                    GPIO.output(self.green, GPIO.LOW)
                self.blink(self.red)
                trigger0 = True
            if ldr_value <= self.triggerThreshold and ldr_value <= self.triggerThreshold and trigger0:
                trigger1 = True
                print('  Triggered...[sensor = %s | threshold = %s]' % (ldr_value,self.triggerThreshold))
            if trigger0 and trigger1:
                print('  RECORDING!')
                print('-' * 25)
                GPIO.output(self.red, GPIO.HIGH)
                GPIO.output(self.green, GPIO.LOW)
                self.time_to_capture(self.file_root)
                trigger0, trigger1 = False, False
                record = True
        return
    
    ## Wrapper function to execute the video capture when light sensor is triggered
    def execute_capture(self,genotype,sex,rep,replicate_number):
        '''Commands needed to appropriately name the file outputs and then begin their recording'''
        self.file_root = genotype + '_' + sex +'_' + self.time_point + '_' + str(rep)
        self.dir_active = self.dir_sex + self.file_root + '/'
        
        print('Creating directory ',self.dir_active)
        self.create_directory(self.dir_active)
        print('%s_%s: Video %s of %s' % (genotype, sex, rep, replicate_number))
        print('  Ready to run...')
        GPIO.output(self.green, GPIO.HIGH)
        self.trigger()
        GPIO.output(self.green, GPIO.LOW)
        return
    
    ## Check-in function to see what user wants following runs of the same genotye-sex combination
    def checkin(self, genotype, sex, rep):
        '''Check-in function to see if user wants more replicates, to recalibrate the light sensor, or to move on'''
        GPIO.output(self.yellow, GPIO.HIGH)
        while True:
            cont = input("Press 'y' to add replicates, <enter> to move on, or 'r' to recalibrate the trigger and then add replicates: ").lower()
            print('=' * 25)
                        
            ## Resetting the trigger threshold
            if cont == 'r':
                ## Resetting trigger threshold
                self.triggerThreshold = self.autocalibrator()
                            
            ## Performing additional replicates
            elif cont == 'y':
                rep += 1
                self.execute_capture(genotype, sex, rep, rep)
                GPIO.output(self.yellow,GPIO.HIGH)
                
            ## Moving onto the next sex-genotype combination
            elif cont == '':
                GPIO.output(self.yellow, GPIO.LOW)
                break
            
            ## Other
            else:
                print('!! Invalid entry')
            
    ## Create directories
    def create_directory(self,path):
        '''Creates a directory if one does not exist'''
        try:
            os.mkdir(path)
        except:
            print('')
        return
    
    ## Prints an opening statement when the program begins
    def print_open(self):
        '''Initial print statements put into a function'''
        print(80*'#' + '\n'+ '## CLIMBING ASSAY '+ 62*'#' + '\n' + 80*'#')
        print('''
  - This script automates video generation for the Drosophila climbing assay
  - For more information and directions on usage, see the corresponding README.txt file
--> BEFORE CONTINUING, ensure the variables are correctly set in the device.py file [lines 36 - 59]

        LED Light code:
        [GREEN]  - Waiting on user to raise and drop the rig
        [YELLOW] - System is waiting for user input or for an internally timed process to finish
        [RED]    - (Flashing) System is waiting for the rig to drop
        [RED]    - (Solid) The camera is in use (solid)        

''')
        return