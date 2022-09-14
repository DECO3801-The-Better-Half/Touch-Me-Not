# Touch-Me-Not
This project aims to provide users with an immersive synesthesia experience in which 
they can touch different materials and they will trigger different sounds. 
To run the code for this project run the main.py file. 
This code can be stopped with a keyboard interrupt by hitting ctrl + C
## Dependencies
- pyserial : ```pip3 install pyserial```
- playsound : ```pip3 install playsound```

playsound is relying on a python 2 subprocess. Please use `pip3 install PyObjC` if you want playsound to run more efficiently.
## main.py
Generates processes to play sounds when a touch is sensed.

## plant_arduino.ino
Processes plant arduino inputs. This code was adapted from an online source. 

## arduino_read.ino
Gets the read inputs from the arduino. 

## Troubleshooting
```[Errno 2] No such file or directory: '/dev/cu.usbmodem1101'```

This issue is related to the port main.py is trying to read the arduino input from. 
The following link should show you how to find the suitable port for your computer: 
https://www.mathworks.com/help/supportpkg/arduinoio/ug/find-arduino-port-on-windows-mac-and-linux.html 

For convenience you may list the port you need to run the code on your computer below:
- **Lauren:** '/dev/tty.usbmodem14201'
- **Peter:** '/dev/cu.usbmodem1101'
