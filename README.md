# Touch-Me-Not
This project aims to provide users with an immersive synesthesia experience in which 
they can touch different materials and they will trigger different sounds. 
To run the code for this project run the main.py file. 
This code can be stopped with a keyboard interrupt by hitting ctrl + C
## Dependencies
- pyserial : ```pip3 install pyserial```
- pygame: ```pip3 install pygame```

## main.py
Generates processes to play sounds when a touch is sensed.

## LED_controller.ino
Uses the capcitive touch inputs of the different objects to light up parts of the LED strip, with different colours and specific LEDs depending on what objects were touched. 

## arduino_read.ino
Gets the read inputs from the arduino. 

## Wiring
1. Orient the breadboard to have wires facing up 
2. Connect the alligator clip to the left side of the resistors

![IMG_6857](https://user-images.githubusercontent.com/88118932/190286986-9709f1e9-f6db-4a0d-9529-1fef5aa7de49.jpg)


## Troubleshooting
```[Errno 2] No such file or directory: '/dev/cu.usbmodem1101'```

This issue is related to the port main.py is trying to read the arduino input from. 
The following link should show you how to find the suitable port for your computer: 
https://www.mathworks.com/help/supportpkg/arduinoio/ug/find-arduino-port-on-windows-mac-and-linux.html 

For convenience you may list the port you need to run the code on your computer below:
- **Lauren:** '/dev/tty.usbmodem14201'
- **Peter:** '/dev/cu.usbmodem1101'
