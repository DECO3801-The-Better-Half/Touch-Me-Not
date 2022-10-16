import serial
import pygame
import os
import glob
from pprint import pprint
from instrument import *
from arduino_serial import ArduinoSerial

PRESSED = True
UNPRESSED = False

TICKS_PER_SECOND = 30

# To change which input plays which sound, modify this list
# The first input plays SOUNDS[0], second SOUNDS[1], etc.
SOUNDS_PATH = ['sounds/plant.wav', 'sounds/water.wav', 'sounds/light.wav', 'sounds/fabric.wav']

# List of instrument names, in order of output from serial
INSTRUMENT_NAMES_LEFT = [
    "Left lamp",
    "Left flower",
    "Left dragonfly",
    "Left plant 2",
    "Left plant 1"  # far left
]

INSTRUMENT_NAMES_RIGHT = [
    "Right lamp",
    "Right water",
    "Right plant 2",
    "Right plant 1",
    "Right flower",
]

BASE_THRESHOLD = 500
LAMP_THRESHOLD = 800

left_instruments = [
    Instrument("Left lamp", "lightL", threshold=LAMP_THRESHOLD),
    Instrument("Left flower", "flowerL", threshold=BASE_THRESHOLD),
    Instrument("dragonfly", "dragonfly", threshold=BASE_THRESHOLD),
    Instrument("Left plant 2", "plantFL", threshold=BASE_THRESHOLD),
    Instrument("Left plant 1", "plantL", threshold=BASE_THRESHOLD),
]

right_instruments = [
    Instrument("Right lamp", "lightR", threshold=LAMP_THRESHOLD),
    Instrument("Water", "water", threshold=BASE_THRESHOLD),
    Instrument("Right flower", "flowerR", threshold=BASE_THRESHOLD),
    Instrument("Right plant 2", "plantFR", threshold=BASE_THRESHOLD),
    Instrument("Right plant 1", "plantR", threshold=BASE_THRESHOLD),
    Instrument("Right flower", "flowerR", threshold=BASE_THRESHOLD),
]

all_instruments = left_instruments + right_instruments

PORT_ONE = '/dev/cu.usbserial-1410'
PORT_TWO = '/dev/cu.usbmodem14201'

pygame.init()

thisdir = os.getcwd()
sound_dir_path = thisdir + "/audio/*"
sound_files_paths = glob.glob(sound_dir_path)

# Retrieve the different sounds from sound_files_paths
sound_objects = {}
for sound in sound_files_paths:
    abs_path = os.path.basename(sound)  # Get sound file name without path
    instrument = abs_path.split('_')[0]  # Get instrument type (e.g. water)
    type = abs_path.split("_")[1]  # e.g. hold, impact
    key = abs_path.split("_")[2]  # e.g. A, C

    sound_objects[(instrument, type)] = pygame.mixer.Sound(sound)

# Give these sounds to each instrument.
sound_classes = []
for (name, type), sound_object in sound_objects.items():
    # instrument_object = Instrument(name)

    # Find instrument that has that file_name
    for instrument in all_instruments:
        if instrument.file_name == name:
            if type == "impact":
                instrument.add_impact(sound_object)
            elif type == "hold":
                instrument.add_hold(sound_object)

    # if instrument_object not in sound_classes:
    #     sound_classes.append(instrument_object)

    # for instrument in sound_classes:
    #     if instrument.name == name:
    #         if type == "impact":
    #             instrument.add_impact(sound_object)
    #
    #         if type == "hold":
    #             instrument.add_hold(sound_object)

# Duplicate objects

pprint(sound_classes)
pprint(all_instruments)

# plant_sound1 = pygame.mixer.Sound('Sounds/plant.wav')
# water_sound1 = pygame.mixer.Sound('Sounds/water.wav')
# light_sound1 = pygame.mixer.Sound('Sounds/light.wav')
# fabric_sound1 = pygame.mixer.Sound('Sounds/fabric.wav')
# guitar_sound1 = pygame.mixer.Sound('Sounds/short-guitar-riff.wav')
#
# plant_sound2 = pygame.mixer.Sound('Sounds/plant.wav')
# water_sound2 = pygame.mixer.Sound('Sounds/water.wav')
# light_sound2 = pygame.mixer.Sound('Sounds/light.wav')
# fabric_sound2 = pygame.mixer.Sound('Sounds/fabric.wav')
# guitar_sound2 = pygame.mixer.Sound('Sounds/short-guitar-riff.wav')
#
# SOUNDS1 = [light_sound1, plant_sound1, water_sound1, guitar_sound1, fabric_sound1]
# SOUNDS2 = [light_sound2, plant_sound2, water_sound2, guitar_sound2, fabric_sound2]
#
# SOUNDS_COMBINED = []
# SOUNDS_COMBINED.extend(SOUNDS1)
# SOUNDS_COMBINED.extend(SOUNDS2)

clock = pygame.time.Clock()

def get_serial():

    #run to get port on MacOs 'ls -l /dev/cu.usb*'
    # sPort1 = PORT_ONE
    # ser1 = serial.Serial(sPort1, 9600, timeout=1)
    # data1 = ser1.readline()
    #
    # sPort2 = PORT_TWO
    # ser2 = serial.Serial(sPort2, 9600, timeout=1)
    # data2 = ser2.readline()

    ser1 = ArduinoSerial(left_instruments, PORT_ONE)
    ser2 = ArduinoSerial(right_instruments, PORT_TWO)

    states = []  # Playing or not, not needed with class
    thresholds = [800, 200, 200, 200, 200, 800, 200, 200, 200, 200]
    # Easy

    # Recording functions
    # records = []
    # recording = False
    # records_size = 0
    # record_start_time = 0
    #
    # play_rec = False
    # play_index = 0
    # play_start_time = 0

    parsed_data = None
    parsed_data1 = None
    parsed_data2 = None

    while True:

        ticks = pygame.time.get_ticks()  # Used for recording function
        #print(ticks)

        # for event in pygame.event.get():  # Keypresses for recording
        #
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_a:  # Pressing a records
        #             recording = not recording
        #             if recording:
        #                 record_start_time = ticks
        #                 print("recording started")
        #             else:
        #                 print((ticks - record_start_time)/1000)
        #                 print("recording stopped")
        #                 records_size = len(records)
        #
        #         if event.key == pygame.K_s:  # Pressing S plays back
        #             play_rec = not play_rec
        #             if play_rec:
        #                 play_start_time = ticks
        #                 print("playing started")
        #             else:
        #                 print("playing stopped")

        parsed_data_one = ser1.get_serial()
        parsed_data_two = ser2.get_serial()

        # if ser1.inWaiting() > 0:  # read from arduino
        #     # Read data from serial
        #     data1 = ser1.readline()
        #     parsed_data1 = data1.decode().strip().split(" ")
        #     #print("arduino 1: ", parsed_data1)
        #
        # if ser2.inWaiting() > 0:  # Read from arduino
        #     # Read data from serial
        #     data2 = ser2.readline()
        #     parsed_data2 = data2.decode().strip().split(" ")
        #     #print("arduino 2: ", parsed_data2)

        # if parsed_data1 and parsed_data2:  # If both are read, create fresh data
        #     #    print("arduino 1: ", parsed_data1, "arduino 2: ", parsed_data2)
        #     parsed_data = list()
        #     parsed_data.extend(parsed_data1)
        #     parsed_data.extend(parsed_data2)
        #     print(parsed_data)

        # if recording:
        #     records.append(parsed_data)
        #
        # if play_rec:
        #     if play_index < records_size:
        #         parsed_data = records[play_index]
        #     elif play_index == records_size:
        #         print("playing finished")
        #         play_rec = False
        #         print((ticks - play_start_time) / 1000)
        #     play_index += 1

        if parsed_data_one:
            for instrument, value in parsed_data_one:
                if value >= instrument.threshold:
                    instrument.play()
                else:
                    instrument.stop()

        if parsed_data_one:
            for instrument, value in parsed_data_one:
                if value >= instrument.threshold:
                    instrument.play()
                else:
                    instrument.stop()

        # if parsed_data:  # If there is read data
        #     # Check that thread and state lists are correct size
        #     # while len(parsed_data) > len(states):
        #     #     states.append(UNPRESSED)
        #
        #     for i in range(len(parsed_data)):
        #         value = int(parsed_data[i])
        #
        #         if (value > thresholds[i] or value == -2) and states[i] != PRESSED:
        #             states[i] = PRESSED
        #
        #             SOUNDS_COMBINED[i].play(loops=-1)
        #
        #     for i in range(len(parsed_data)):
        #         value = int(parsed_data[i])
        #         if (value <= thresholds[i] and value != -2) and states[i] == PRESSED:
        #             states[i] = UNPRESSED
        #
        #             SOUNDS_COMBINED[i].stop()

        clock.tick(TICKS_PER_SECOND * 3)  # Frame rate in pygame


if __name__ == '__main__':
    get_serial()
