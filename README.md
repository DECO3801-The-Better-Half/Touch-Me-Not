# Touch-Me-Not
This project aims to provide users with an immersive synesthesia experience in which 
they can touch different materials which trigger different sounds. 

To run the code for this project:
- Upload `LED_controller/left_LED_controller/left_LED_controller.ino` to one Arduino Uno board
- Upload `LED_controller/right_LED_controller/right_LED_controller.ino` to another Arduino Uno board
- Wire these boards in accordance to the wiring diagram [##### TODO give diagram ####]
- Connect these boards to your computer via USB
- Set the port names of these devices in `main.py` (TODO improve wording)
- Run `main.py` using python

This code can be stopped with a keyboard interrupt by hitting ctrl + C (command + c for mac users).

## Dependencies
- python: Version >= 3.8
- pyserial : ```pip3 install pyserial```
- pygame: ```pip3 install pygame```

## main.py
Take serial input from the Arduinos and play audio according to that input.

## LED_controller.ino
Uses the capacitive touch inputs of the different instruments to light up parts of the LED strip and send values via serial, with different colours and specific LEDs depending on what objects were touched.

## arduino_read.ino
Gets the read inputs from the arduino. 

## Wiring
1. Orient the breadboard to have wires facing up 
2. Connect the alligator clip to the left side of the resistors

![IMG_6857](https://user-images.githubusercontent.com/88118932/190286986-9709f1e9-f6db-4a0d-9529-1fef5aa7de49.jpg)

## Troubleshooting
```[Errno 2] No such file or directory: '/dev/cu.usbmodem1101'```

This issue is related to the port main.py is trying to read the arduino input from.
[Follow this link to find the suitable port for your computer.](https://www.mathworks.com/help/supportpkg/arduinoio/ug/find-arduino-port-on-windows-mac-and-linux.html)

Once you find the correct ports, update the `PORT_ONE` AND `PORT_TWO` constants in`main.py`.

For convenience, you may list the port you need to run the code on your computer below:
- **Lauren:** '/dev/tty.usbmodem14201'
- **Peter:** '/dev/cu.usbmodem1101'

## Definitions
_Instrument_: An object, like plant or flower, giving input to the Arduino.

_Arduino_: A microcontroller used to read our instruments and send data to the computer via serial.
