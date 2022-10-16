import serial
import pygame
import os
import glob
from instrument import *
from arduino_serial import ArduinoSerial
from sound import Sound
from pprint import pprint

TICKS_PER_SECOND = 30

BASE_THRESHOLD = 800

PORT_ONE = '/dev/cu.usbserial-1420'
PORT_TWO = '/dev/cu.usbmodem14101'

CAPACITANCE_OVERFLOW = -2

KEY = "G_sharp_major.wav"

def main():
    pygame.init()

    this_dir = os.getcwd()
    sound_dir_path = this_dir + "/audio/*"
    sound_files_paths = glob.glob(sound_dir_path)

    # Retrieve the different sounds from sound_files_paths
    sound_objects = {}
    for sound in sound_files_paths:
        abs_path = os.path.basename(sound)  # Get sound file name without path
        instrument, type, key = abs_path.split("_", 2)
        # e.g. water, hold, f_harmonic_minor

        sounds = sound_objects.get((instrument, type), [])
        sounds.append(Sound(sound, f"{instrument}_{type}_{key}", key))
        sound_objects[(instrument, type)] = sounds

    # Initialise our instruments in the right order so ArduinoSerial can read them
    left_instruments = [
        Instrument("Left lamp", "lightL", threshold=BASE_THRESHOLD),
        Instrument("Left flower", "flowerL", threshold=BASE_THRESHOLD),
        Instrument("Dragonfly", "dragonfly", threshold=BASE_THRESHOLD),
        Instrument("Left plant 2", "plantFL", threshold=BASE_THRESHOLD),
        Instrument("Left plant 1", "plantL", threshold=BASE_THRESHOLD),
    ]

    right_instruments = [
        Instrument("Right lamp", "lightR", threshold=BASE_THRESHOLD),
        Instrument("Water", "water", threshold=BASE_THRESHOLD + 200),
        Instrument("Right plant 2", "plantFR", threshold=BASE_THRESHOLD),
        Instrument("Right plant 1", "plantR", threshold=BASE_THRESHOLD),
        Instrument("Right flower", "flowerR", threshold=BASE_THRESHOLD),
    ]

    all_instruments = left_instruments + right_instruments

    # Give these sounds to each instrument.
    for (name, type), sound_objects in sound_objects.items():
        # Find instrument that has that file_name
        for instrument in all_instruments:
            if instrument.file_name == name:
                if type == "impact":
                    for sound_object in sound_objects:
                        instrument.add_impact(sound_object)
                elif type == "hold":
                    for sound_object in sound_objects:
                        instrument.add_hold(sound_object)

    # Reduce the impact sounds of plants and the dragonfly
    left_instruments[2].set_volume("impact", 0.5)
    left_instruments[3].set_volume("impact", 0.5)
    left_instruments[4].set_volume("impact", 0.5)

    right_instruments[2].set_volume("impact", 0.5)
    right_instruments[3].set_volume("impact", 0.5)
    right_instruments[4].set_volume("impact", 0.5)

    clock = pygame.time.Clock()

    ser1 = ArduinoSerial(left_instruments, PORT_ONE)
    ser2 = ArduinoSerial(right_instruments, PORT_TWO)

    while True:
        serial_data_one = ser1.get_serial()
        serial_data_two = ser2.get_serial()

        for data in (serial_data_one, serial_data_two):
            if data:
                for cur_instrument, value in data.items():
                    if value >= cur_instrument.threshold or value == CAPACITANCE_OVERFLOW:
                        cur_instrument.play(KEY)
                    else:
                        cur_instrument.stop()

        clock.tick(TICKS_PER_SECOND * 3)  # Frame rate in pygame


if __name__ == '__main__':
    main()
