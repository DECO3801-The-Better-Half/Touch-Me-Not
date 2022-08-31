# import cv2
# from cvzone.FaceDetectionModule import FaceDetector
# import matplotlib.pyplot as plt
# from deepface import DeepFace
import time
import serial
import threading
from multiprocessing import Process
from playsound import playsound

import trace
import sys
import wave

PRESSED = True
UNPRESSED = False

PLANT = 0
WATER = 1
LIGHT = 2
FABRIC = 3

# To change which input plays which sound, modify this list
# The first input plays SOUNDS[0], second SOUNDS[1], etc.
SOUNDS = ['sounds/plant.wav', 'sounds/water.wav', 'sounds/light.wav', 'sounds/fabric.wav']

def play(file):
    while True:
        playsound(file, block=True)


def get_serial():

        sPort = '/dev/cu.usbmodem1101'
        ser = serial.Serial(sPort, 9600, timeout=1)



        data = ser.readline()

        states = []
        playing = [True, True, True, True]
        threads = []
        thresholds = [90, 1400, 19000, 200]

        while True:

            if ser.inWaiting() > 0:
                # Read data from serial
                data = ser.readline()
                #print(data)
                parsed_data = data.decode().strip().split(" ")
                print(parsed_data)

                # Check that thread and state lists are correct size
                while len(parsed_data) > len(states):
                    states.append(UNPRESSED)
                while len(parsed_data) > len(threads):
                    threads.append(None)

                # Start a new thread to play the sound for each input
                for i in range(len(parsed_data)):

                    value = int(parsed_data[i])

                    if (value > thresholds[i] or value == -2) and states[i] != PRESSED:
                        states[i] = PRESSED

                        if i == LIGHT:

                            playing[i] = (playing[i] != True)

                            if not playing[i]:

                                threads[i] = Process(target=play, args=(SOUNDS[i],))
                                threads[i].start()


                            else:
                                threads[i].terminate()

                        else:

                            threads[i] = Process(target=play, args=(SOUNDS[i], ))
                            threads[i].start()


                # For each input, change state to unpressed if they are
                # below the threshold
                for i in range(len(parsed_data)):
                    value = int(parsed_data[i])
                    if (value <= thresholds[i] and value != -2) and states[i] == PRESSED:
                        states[i] = UNPRESSED

                        if i != LIGHT:
                            threads[i].terminate()


if __name__ == '__main__':

    #x = threading.Thread(target=get_serial, args=())
    #x.start()
    #x.run()

    # Run below
    #x = pr.Thread(target=get_serial, args=())
    x = Process(target=get_serial, args=())
    x.start()

    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #print(dir_path)
    #playsound('sounds/small-door-bell.wav')
    #playsound('sounds/small-door-bell.wav')
