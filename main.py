"""main.py

Run this file to read serial input from arduinos and turn it into audio.

The port numbers PORT_ONE and PORT_TWO will likely have to be changed to
the ports that each arduino is attached to.
"""

import os
import glob
from typing import Tuple, Dict, List
import pygame

from instrument import Instrument
from arduino_serial import ArduinoSerial
from sound import Sound

TICKS_PER_SECOND = 30

BASE_THRESHOLD = 800

PORT_ONE = '/dev/cu.usbserial-10'  # '/dev/cu.usbserial-1420'
PORT_TWO = '/dev/cu.usbmodem1101'  # '/dev/cu.usbmodem14101'

CAPACITANCE_OVERFLOW = -2

KEY = "G_sharp_major.wav"


def get_audio() -> Dict[Tuple[str, str], List[Sound]]:
    """Return a mapping of instruments to Sounds

    Returns:
        mapping: (instrument, music_type) -> sounds
        instrument is a string in the file name format (e.g. plantFL)
        music_type is the type of sound (hold or impact)
        sounds is a list of Sound objects
    """
    this_dir = os.getcwd()
    sound_dir_path = this_dir + "/audio/*"
    sound_files_paths = glob.glob(sound_dir_path)

    # Retrieve the different sounds from sound_files_paths
    sound_objects = {}
    for sound in sound_files_paths:
        abs_path = os.path.basename(sound)  # Get sound file name without path
        instrument, music_type, key = abs_path.split("_", 2)
        # e.g. water, hold, f_harmonic_minor

        sounds = sound_objects.get((instrument, music_type), [])
        sounds.append(Sound(sound, f"{instrument}_{music_type}_{key}", key))
        sound_objects[(instrument, music_type)] = sounds

    return sound_objects


def main():
    """Run the main loop"""
    pygame.init()

    sound_objects = get_audio()

    # Initialise our instruments in the right order so ArduinoSerial can read
    left_instruments = [
        Instrument("Left lamp", "lightL", threshold=BASE_THRESHOLD),
        Instrument("Left flower", "flowerL", threshold=BASE_THRESHOLD),
        Instrument("Dragonfly", "dragonfly", threshold=BASE_THRESHOLD),
        Instrument("Left plant 2", "plantFL", threshold=BASE_THRESHOLD),
        Instrument("Left plant 1", "plantL", threshold=BASE_THRESHOLD),
    ]

    right_instruments = [
        Instrument("Right lamp", "lightR", threshold=BASE_THRESHOLD),
        Instrument("Water", "water", threshold=BASE_THRESHOLD + 1000),
        Instrument("Right plant 2", "plantFR", threshold=BASE_THRESHOLD),
        Instrument("Right plant 1", "plantR", threshold=BASE_THRESHOLD),
        Instrument("Right flower", "flowerR", threshold=BASE_THRESHOLD),
    ]

    all_instruments = left_instruments + right_instruments

    # Give these sounds to each instrument.
    for (name, touch_type), sounds in sound_objects.items():
        # Find instrument that has that file_name
        for instrument in all_instruments:
            if instrument.file_name == name:
                if touch_type == "impact":
                    for sound in sounds:
                        instrument.add_impact(sound)
                elif touch_type == "hold":
                    for sound in sounds:
                        instrument.add_hold(sound)

    # Adjust volumes
    left_instruments[1].set_volume("hold", 0.5)
    left_instruments[1].set_volume("impact", 0.5)
    right_instruments[4].set_volume("hold", 0.5)
    right_instruments[4].set_volume("impact", 0.5)

    left_instruments[0].set_volume("hold", 0.7)
    left_instruments[0].set_volume("impact", 0.7)
    right_instruments[0].set_volume("hold", 0.7)
    right_instruments[0].set_volume("impact", 0.7)

    left_instruments[3].set_volume("hold", 0.7)
    left_instruments[3].set_volume("impact", 2)
    left_instruments[4].set_volume("hold", 0.7)
    left_instruments[4].set_volume("impact", 2)

    right_instruments[2].set_volume("hold", 0.7)
    right_instruments[2].set_volume("impact", 2)
    right_instruments[3].set_volume("hold", 0.7)
    right_instruments[3].set_volume("impact", 2)

    clock = pygame.time.Clock()

    ser1 = ArduinoSerial(left_instruments, PORT_ONE)
    ser2 = ArduinoSerial(right_instruments, PORT_TWO)

    while True:
        serial_data_one = ser1.get_serial()
        serial_data_two = ser2.get_serial()

        for data in (serial_data_one, serial_data_two):
            if data:
                for cur_instrument, value in data.items():
                    if value >= cur_instrument.threshold \
                            or value == CAPACITANCE_OVERFLOW:
                        cur_instrument.play(KEY)
                    else:
                        cur_instrument.stop()

        clock.tick(TICKS_PER_SECOND * 3)  # Frame rate in pygame


if __name__ == '__main__':
    main()
