# Touch-Me-Not
This project aims to provide users with an immersive synesthesia experience in which 
they can touch different materials and they will trigger different sounds. 
To run the code for this project run the main.py file. 
This code can be stopped with a keyboard interrupt by hitting ctrl + C

## Dependencies
- pyserial : ```pip3 install pyserial```
- pygame: ```pip3 install pygame```

## Subsystems
main.py
	Generates and processes to play sounds when a touch is sensed.
LED_controller.ino
	Uses the capacitance touch sensors and light sensors of the different objects to light up parts of the LED strip, with different colours and specific LEDs depending on what objects were touched.
arduino_read.ino
	Gets the read inputs from the Arduino. 
sound_generator.py
	Generates a library of sounds from a given jobfile using the samples in audio_generator/sound_components.
	Generatores an instruction file for main.py to use in filename selection.

## Installation
1. Connect the Arduinos capacitance and light sensors to the objects and plug LEDs into Arduinos according to the.
	### Wiring
	1. Orient the breadboard to have wires facing up 
	2. Connect the alligator clip to the left side of the resistors
	![IMG_6857](https://user-images.githubusercontent.com/88118932/190286986-9709f1e9-f6db-4a0d-9529-1fef5aa7de49.jpg)
2. Load and run synthesia_control.ino and arduino_read.ino on the Arduinos.
3. Plug the two Arduino USB cables into the comoputer and note the port names (see Troubleshooting).

## Usage
### main.py
	usage: python3 main.py [username] [-m cooldown] [-k]
		username: name of new or existing user
			(used to select port names)
		-m cooldown: use modulation mode with modulation cooldown period in seconds
			(changes musical key when an object is touch after cooldown period)
		-k: use keyboard keys 0-9 to represent object touches instead of Arduino input
			(may not work on systems with incompatible key mappings)


## Troubleshooting
```[Errno 2] No such file or directory: '/dev/cu.usbmodem1101'```

This issue is related to the port main.py is trying to read the arduino input from. 
The following link should show you how to find the suitable port for your computer: 
https://www.mathworks.com/help/supportpkg/arduinoio/ug/find-arduino-port-on-windows-mac-and-linux.html 

For convenience you may list the port you need to run the code on your computer below:
- **Lauren:** '/dev/tty.usbmodem14201'
- **Peter:** '/dev/cu.usbmodem1101'
