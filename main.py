import serial
import pygame
import os
import glob
from instrument import *
from arduino_serial import ArduinoSerial

TICKS_PER_SECOND = 30

BASE_THRESHOLD = 500
LAMP_THRESHOLD = 800

PORT_ONE = '/dev/cu.usbserial-1410'
PORT_TWO = '/dev/cu.usbmodem14201'

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

        sound_objects[(instrument, type)] = pygame.mixer.Sound(sound)

    # Initialise our instruments
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

    # Give these sounds to each instrument.
    sound_classes = []
    for (name, type), sound_object in sound_objects.items():
        # Find instrument that has that file_name
        for instrument in all_instruments:
            if instrument.file_name == name:
                if type == "impact":
                    instrument.add_impact(sound_object)
                elif type == "hold":
                    instrument.add_hold(sound_object)

    clock = pygame.time.Clock()

    ser1 = ArduinoSerial(left_instruments, PORT_ONE)
    ser2 = ArduinoSerial(right_instruments, PORT_TWO)

    while True:
        serial_data_one = ser1.get_serial()
        serial_data_two = ser2.get_serial()

        if serial_data_one:
            for cur_instrument, value in serial_data_one.items():
                if value >= cur_instrument.threshold:
                    cur_instrument.play()
                else:
                    cur_instrument.stop()

        if serial_data_two:
            for cur_instrument, value in serial_data_two.items():
                if value >= cur_instrument.threshold:
                    cur_instrument.play()
                else:
                    cur_instrument.stop()

        clock.tick(TICKS_PER_SECOND * 3)  # Frame rate in pygame


if __name__ == '__main__':
    main()
