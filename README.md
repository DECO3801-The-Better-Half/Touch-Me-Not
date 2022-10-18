# Touch-Me-Not
This project aims to provide users with an immersive synesthesia experience in which 
they can touch different materials and they will trigger different sounds. 
To run the code for this project run the main.py file. 
This code can be stopped with a keyboard interrupt by hitting ctrl + C

## Subsystems
### Synaesthesia Experience
main.py
	Plays sounds using pre-processed output of sound_generator.py and sensor values from the arduino.
LED_controller.ino
	Uses the capacitance touch sensors and light sensors of the different objects to light up parts of the LED strip, with different colours and specific LEDs depending on what objects were touched.
arduino_read.ino
	Gets the read inputs from the Arduino. 
### Generate Audio
sound_generator.py
	Generates a library of sounds from a given jobfile using the samples in audio_generator/sound_components.
	Generatores an instruction file for main.py to use in filename selection.

## Dependencies
### Synaesthesia Experience
- python3: see https://www.python.org/downloads/
- pyserial: ```pip3 install pyserial```
- pygame: ```pip3 install pygame```
### Generate Audio
- zsh: see https://www.zsh.org/
- sox: see https://sox.sourceforge.net/

## Installation
1. Connect the Arduinos capacitance and light sensors to the objects and plug LEDs into Arduinos.
	### Wiring
	1. Orient the breadboard to have wires facing up 
	2. Connect the alligator clip to the left side of the resistors
	![IMG_6857](https://user-images.githubusercontent.com/88118932/190286986-9709f1e9-f6db-4a0d-9529-1fef5aa7de49.jpg)
2. Load and run synthesia_control.ino and arduino_read.ino on the Arduinos.
3. Plug the two Arduino USB cables into the comoputer and note the port names (see Troubleshooting).
4. If mac or linux OS, run "chmod +x start.sh"
5. Install dependancies

## Usage
### Synaesthesia Experience
Unix-based`
Usage: ```./start.sh [username] [-m cooldown] [-k]```
	username: name of new or existing user
		(used to select port names)
	-m cooldown: use modulation mode with modulation cooldown period in seconds
		(changes musical key when an object is touch after cooldown period)
	-k: use keyboard keys 0-9 to represent object touches instead of Arduino input
		(may not work on systems with incompatible key mappings)

Directly through python3
Usage: ```python3 main.py [username] [-m cooldown] [-k]```
	username: name of new or existing user
		(used to select port names)
	-m cooldown: use modulation mode with modulation cooldown period in seconds
		(changes musical key when an object is touch after cooldown period)
	-k: use keyboard keys 0-9 to represent object touches instead of Arduino input
		(may not work on systems with incompatible key mappings)

### Generate Audio: Generate
Exectute in audio_generator directory. Only works on unix-based OS with sox installed.
Usage: ```python3 generate_sounds.py jobfile```
	jobfile: file specifying the instruments, their sounds, and the layers of each sounds.
		(instruments correspond to objects, layers are the wav files comprising each sound, see Generate audio: jobfile)

### Generate Audio: Jobfile:
The jobfile tells the audio generator what sounds to make and how to edit them.

Define instruments first: 
	instrument instrument_name key range_mode balance
		instrument_name: name of the object
		key: musical key associated with the object
		range_mode: range of sounds to generate for object (chord, scale, or arpeggio)
		balance: left-right balance of the object's generated sounds in format LxRy where x and y are the volume scale factor of each of the wav's stereo channels
e.g. 
"
instrument water C_sharp_major chord L1R1
"

Then define sounds with their layers listed below
	sound instrument_name sound_name sound_volume_scale_factor
	- filename note layer_volume_scale_factor
	- ...
		instrument_name: name of the object this sound is assigned to
		sound_name: name of the sound (impact or hold)
		sound_volume_scale_factor: scale factor for the volume of this sound (applied after layers are merged)
		filename: name of the layer's filename
		note: note of the layer in format, "X_sharp", for the semitone above note X
		volume_scale_factor: scale factor for the volume of this wav file
e.g.
"
sound flowerR hold 1.2
- sound_components/Flower/sparky_drone_G#.wav G_sharp 0.5
- sound_components/Flower/vocals_G.wav G 1.5
- sound_components/Flower/bees.wav none 0.1
"

Lines beginning with anything other than "instrument", "sound", or "-" will be ignored.

## Troubleshooting
```[Errno 2] No such file or directory: '/dev/cu.usbmodem1101'```

This issue is related to the port main.py is trying to read the arduino input from. 
The following link should show you how to find the suitable port for your computer: 
https://www.mathworks.com/help/supportpkg/arduinoio/ug/find-arduino-port-on-windows-mac-and-linux.html 

For convenience you may list the port you need to run the code on your computer below:
- **Lauren:** '/dev/tty.usbmodem14201'
- **Peter:** '/dev/cu.usbmodem1101'