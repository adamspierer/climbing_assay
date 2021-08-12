# Drosophila Climbing Assay

Written August 5, 2021 by Adam Spierer

## Motivation:

The goal of this set of scripts is to automate the process of collecting videos of flies in a climbing performance assay and to standardize the file naming convention. The assay will take in user-defined variables for experimental details (ex. genotypes, sexes, etc) and variables for recording the videos (ex. number of replicates, recording length, etc). The scripts here also automate the recording process, so videos begin recording as soon as flies are "knocked down."

<img src="https://github.com/adamspierer/climbing_assay/blob/main/images/climbing_rig.png" width="600" height="200" align="center">

## Quickstart

<ol>
	<li>Go to the `climbing_assay` directory and open the `device.py` file.</li>
	<li>Modify the `defining_variables` function [lines 36 - 59] in a text editor to match experimental protocol. Save and exit.</li>
	<li>Right click on `climbing_assay.py` and select `Thonny Python IDE`. Press run and proceed from instructions.</li>
	<li>Perform experiment</li>
</ol>

## Program overview

The climbing assay is broken into three scripts. The main script `climbing_assay.py` calls on the other two scripts (`device.py` and `MCP3008.py`). The `device.py` script contains variables the user will likely want to change and the main functions that the `climbing_assay.py` script calls on, while the `MCP3008.py` script contains code for the analog-digital converter to run properly. Raspberry Pis can only read digital signals (on-off), but this chip allows them to read pseudo-analog signals (ex. light sensor).

## Preparing for the assay:

### Putting flies in the climbing rig:
Users will need to transfer the flies from the vials with food, to an empty, clean, and clear glass vial. Vials are inserted with the flug up into the holes in the climbing rig. Make sure to have the vials in the same order if assaying vials multiple times over experimental days. Also take care to ensure that the bottom of the flug matches up with the bottom of the plastic on the top bracket of the climbing rig (so no flies can hide from the camera).

<img src="https://github.com/adamspierer/climbing_assay/blob/main/images/flug_position.png" width="285" height="400" align="center">

Ideally, the user would have the same number of vials for each of the treatments/conditions/genotypes that are being tested. This is important because FreeClimber (analysis program downstream of this) operates under the assumption that there is a consistent number of vials. This can be worked around if necessary by analyzing the videos with different vial numbers with a separate configuration file (change variable for number of vials), but is easier to fix at this stage.

### Turning on the Pi and lightboard:
Make sure the Raspberry Pi is turned on. Since there is no power button, plug the power cord into the Pi. If it is plugged in but no power, then unplug and replug and it should start up within a few seconds. The boot time is about 20-60 seconds.

<img src="https://github.com/adamspierer/climbing_assay/blob/main/images/RPi_fromTop.png" width="400" height="300" align="center">

To turn on the light board, press the icon at the corner of the board shared by the origin of the two rulers. The brightness is important, and if done incorrectly, it can result in a "wagonwheel effect" where alternating dark and light bands move up the video. FreeClimber can still work with banded videos, but the detector works better without the banding. To get the brightness adjusted correctly, navigate to the directory containing `preview.py` and type:

`python preview.py`
	
The program will print out basic instructions when it is run. To eliminate banding patterns that occur due to the shutter speed of the camera matching the flicker rate of the LED, touch and hold the aforementioned icon while running the preview.py script and adjust until the banding disappears. Exit the program by entering 0 or an empty string <enter> into the terminal.

### Making the program specific to an experiment:

There are several variables in the `device.py` script that can be modified. Some are basic to the assay (saving paths, recording parameters, experimental conditions), but others are advanced and correspond with the hardware configuration (sensor pins, LED pins, trigger sensitivities). Both can be changed, but the basic will not affect the main functionality of the program while the advanced will.

Important variables that should be modified for each experiment:
Open the `device.py` script located in: Desktop > climbing_assay > device.py. Right click the program and select the 'Thonny Python IDE'. This will open up a window with the script on top and a shell below. Navigate to the OPTIONS section and look over the basic options for "experimental conditions" and "recording parameters".

The experimental parameters include the nuclear and mitochondrial genotypes. Each permutation will be created with the nuclear genotype starting as the first set with each mitochondrial genotype, followed by the next set. Individual genotypes can be added as items in a list ['example1','example2',...,'examplen'] to the 'extra\_genotypes' variable and will be added to the end of all the permuted combinations. Finally, specific combinations the user does not want to include can be added to the 'delete\_genotypes' list. These will be excluded from the final list of genotypes, which are output in the shell shortly after the `climbing_assay.py` program is run (also in Thonny Python IDE.

IMPORTANT! Filenames will have underscore ('\_') delimiters separating experimental details meant to be parsed later on. This is important because FreeClimber assumes experimental details are separated by '_' and will overlook other delimiters (e.g. ; , . -). So if the user decides to add in an extra experimental detail, it must contain an underscore if it is meant to be separated later on.

Recording parameters should also be considered, especially `dir_home`, which corresponds with the main experiment folder that might be used in a longer term or longitudinal experiment. There is an opportunity in the program to create folders for individual days of experimentation, but the 'dir\_home' variable sets the parent folder for these. The other options for `capture\_time` (recommended 5 seconds), `wait\_time` (recommened 10 seconds), and `replicate_number` for each set of knockdowns (recommended 3 or 4), can also be changed. 

Advanced options for the `trigger\_sensitivity` can be changed where the trigger is activated if (`sensor_value > avgLow * trigger_sensitivity`). At `trigger\_sensitivity = 5`, the photosensor needs to exceed 5 x the average low value in order to trigger. For `n_samples_for_trigger_calibration`, the value represents the number of samples to collect for calibrating the phototrigger. These values are generally consistent between the time points, but the average between them gives a better value.

The other advanced options are for the pins used by the Pi. It is set to `channel` 0 for the analog-digital converter (ADC; [MCP3008 chip](https://tutorials-raspberrypi.com/mcp3008-read-out-analog-signals-on-the-raspberry-pi/)). This is the upper left most pin on the chip (with the semi circle in the middle pointing up). These pins go 0-7 (top to bottom) and the wire that is between the photoresistor and the other resistor should plug into the apropriate chip pin row on the breadboard. The other pins correspond with the colored LED on the Raspberry Pi. Raspberry Pi pins are numbered in the code according to their physical location on the GPIO board (numbered 1-40). The cobbler (adapter) that interfaces between the actual pins and the breadboard is labeled according to the pin names. These names are different from the pin numbers, so one should checkout a "Raspberry Pi pinout" to figure out the pin number-to-name conversion.

Once these variables are modified, the user is good to run the experiment!


## Running the assay -- Beginning program

#### Raspberry Pi GUI:

1. Navigate to the `climbing_assay` directory. Right click `climbing_assay.py` and select 'Thonny Python IDE'. Click the `Run` button on the top menu.

#### Terminal:

1. Type:
`python3 <full_path_to_climbing_assay.py>`

*NOTE*: The current Raspberry Pi build has trouble when running the climbing assay from the command line. If Python 3.5+ were installed then it could theoretically work from the command line.

## Running the assay -- Configuring run

*IMPORTANT!* The phototrigger is light dependent and will respond differently if there is ambient light vs. not. For best results, reduce ambient light by turning off the lights.

Put glass vials of flies (10-25 flies per vial) into the climbing rig with the light blocker in front of the light sensor (black 1.5mL tube).

When the program goes through its setup process, it will ask you to raise and lower the climbing rig. This step is important for calibrating the phototrigger. It will come up with a threshold of its own that is the halfway point between the raised and lowered values.

Next, the program will tell you what directory you are in and ask if you want to save this round of videos to an existing folder (good for keeping time series experiments together) or create a new one (new time series experiment). If you decide to create a new one, it will prompt the user for a directory name.

The program will ask what day the experiment is, because it assumes the user is doing a longitudinal experiment. If there is no day or longitudinal component, the user can enter a '0' which will act as a placeholder but still be included in the directory and file names throughout.

The program will then ask how long the user wants to preview the camera view for. This is helpful for ensuring that the setup is aligned properly (good view of all flies with minimal interference). When finished with this step, enter '0' or <enter> and the assay will begin.

## Running the assay -- Running the flies

By this point, the assay is ready to run (indicated by the green LED turning on--this is the weakest of the lights). The mitotype, genotype, and sex will be displayed, as well as the path to the save directory (for the video file and an image of the end of the assay).

Raise the climbing rig to about 7 cm from the platform (highest sharpie mark on the aluminum rod) and the system will arm itself. This is noted by text in the shell and red light flashing. When the rig is dropped, the red light will become solid to indicate that the video is recording and the shell will print a statement acknowledging this. With a slight delay, a live feed of the camera will appear on the screen showing what the camera sees. When the feed ends and the light switches to yellow, the recording is finished and the program enters into the 'wait_time' period specified by the user in the basic options at the top of the script. This is a chance for the flies to recover and collect their thoughts before climbing again. When the program is ready, it will say so in the shell and the green light will turn on.

After the specified number of replicates is completed, the program will ask if the user wants to run more replicates (`y`), recalibrate the light sensor (`r`), or continue (`<enter>`) are in order or to continue. If `y` is selected, then the program will record a single video when the user is ready. If `r` is selected, the program will prompt the user to raise and lower the rig. On occasion, the sensor gets jostled and the sensor value becomes different from what it was originally calibrated against. 

Only after the user presses `<enter>` will the program continue until there are no more conditions left to record. The program will end and the LED lights will turn off (but not the light box, which must be turned off manually).

At this point, the resulting video files can be transfered to a USB drive or uploaded to OSCAR. 

If uploading to OSCAR, make sure the internet is turned on (WiFi symbol on upper right of menu) and open a web browser window. Go to any web site to receive a prompt for getting the network to ask for guest permission.

Type:
`scp -r <path_to_batch_folder> <drand@ssh.ccv.brown.edu:/users/drand/data/dfscreen/climbing/>`

It might be necessary to login to OSCAR first to create a batch folder to transfer the files, or they can be moved afterward.

## Running FreeClimber 

Download [FreeClimber](https://github.com/adamspierer/FreeClimber) from the Github page and follow directions in the Tutorial page.

If using in the Rand lab, go to the OSCAR directory: /users/drand/data/drand/dfscreen/climbing/ and copy the configuration file (`deficiency_screen.cfg`) to the new directory containing all the new files. Use `nano` to access this file and edit the `project_path` field to reflect the path to the folder just uploaded. Grab the full path to the configuration file and navigate to the `freeclimber` folder. 

To run FreeClimber on OSCAR, type:
`sbatch /users/drand/data/dfscreen/freeclimber/freeclimb.sh <path_to_recently_created_configuration_file>`

Alternatively, specify the path to the configuration file in the script itself, though this is much more tedious and the script can handle either approach.

Either way, running this command will send the job to OSCAR with however many GB of memory and time constraints specified in the bash file. It will process videos at ~15 seconds a piece and output a final `results.csv` file in the `project_path` directory specified in the configuration file.

The results files from all batches can be concatenated together by running:
`module load python/3.7.4`
`python3 ~/data/drand/dfscreen/climbing/concatenate_results.py`

## Troubleshooting

If there is an error with the hardware, the circuit diagram is provided here:

<img src="https://github.com/adamspierer/climbing_assay/blob/main/images/wiring_comparison.png" width="600" height="200" align="center">

On the left is the circuit diagram, the center is a PCB board with the electronics soldered on to ensure a strong connection, and the right is a breadboard with the components and wires hooked up to a Raspberry Pi Cobbler to help organize the pins. The PCB board version has the individual wires labeled with the pin number and what it corresponds with. The table below corresponds with the pin number and name, the function and how it is wired on the circuit board.