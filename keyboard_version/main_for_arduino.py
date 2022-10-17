"""main.py

Run this file to read serial input from arduinos and turn it into audio.

The port numbers PORT_ONE and PORT_TWO will likely have to be changed to
the ports that each arduino is attached to.
"""

from typing import Union
import pygame
import json
import time

from instrument import Instrument
from arduino_serial import ArduinoSerial
from sound import Sound

TICKS_PER_SECOND = 30

BASE_THRESHOLD = 800

MODULATION_COOLDOWN_PERIOD = 5 # seconds

PORT_ONE = '/dev/cu.usbserial-10' #'/dev/cu.usbserial-1420'
PORT_TWO = '/dev/cu.usbmodem1101' # '/dev/cu.usbmodem14101'

CAPACITANCE_OVERFLOW = -2

INSTRUCTION_FILE = "instructions.json"

def get_audio() -> dict[str, dict[str, dict[str, dict[str, Union[Sound, list[Sound]]]]]]:
	"""Return a mapping of instruments to Sound objects
	Returns:
		mapping: sound purpose -> instrument name -> sound type -> music key -> Sound/list[Sound]
		e.g. "normal" -> "lightL" -> "hold" -> "G_sharp_major" -> [Sound, Sound, ...]
		instrument is a string in the file name format (e.g. plantFL)
		type is the type of sound (hold or impact)
		sounds is a list of Sound objects
	"""
	# convert json to dict
	instructions = json.load(open(INSTRUCTION_FILE))
	# replace file names at the end node of the instructions with Sound objects
	for instruments in [instructions["normal"], instructions["pivot"]]:
		for instrument, sound_types in instruments.items():
			for type, music_keys in sound_types.items():
				for music_key, filename_s in music_keys.items():
					if isinstance(filename_s, list):
						music_keys[music_key] = [Sound(filename) for filename in filename_s]
					elif filename_s:
						music_keys[music_key] = Sound(filename_s)
	return instructions

def modulate(old_key: str, new_key: str, all_instruments: list[Instrument], modulating_instrument: Instrument) -> None:
	"""Modulate all instruments to the given key
	Parameters:
		new_key: the key to modulate to
		all_instruments: a list of all instruments
	"""
	print(f"MODULATING TO {new_key}")
	# play pivot chord
	pivot_sound = modulating_instrument.sound_objects["pivot"][modulating_instrument.name]["impact"][old_key]
	print(f"+ {modulating_instrument.name} playing PIVOT CHORD {pivot_sound}")
	pivot_sound.play()
	# change all other instruments to the new key
	for instrument in all_instruments:
		# if the instrument is currently playing, stop it and play it again in the new key
		if instrument._currently_playing:
			instrument.stop()
			instrument.play(new_key, False)

def main():
	"""Run the main loop"""
	print("Initialising...")
	pygame.init()

	current_key = "G_sharp_major"
	last_modulation_time = time.time()
	sound_objects = get_audio()


	# Initialise our instruments in the right order so ArduinoSerial can read them
	left_instruments = [
		Instrument("Left lamp", "lightL", BASE_THRESHOLD, sound_objects),
		Instrument("Left flower", "flowerL", BASE_THRESHOLD, sound_objects),
		Instrument("Dragonfly", "dragonfly", BASE_THRESHOLD, sound_objects),
		Instrument("Left plant 2", "plantFL", BASE_THRESHOLD, sound_objects),
		Instrument("Left plant 1", "plantL", BASE_THRESHOLD, sound_objects),
	]

	right_instruments = [
		Instrument("Right lamp", "lightR", BASE_THRESHOLD, sound_objects),
		Instrument("Water", "water", BASE_THRESHOLD + 200, sound_objects),
		Instrument("Right plant 2", "plantFR", BASE_THRESHOLD, sound_objects),
		Instrument("Right plant 1", "plantR", BASE_THRESHOLD, sound_objects),
		Instrument("Right flower", "flowerR", BASE_THRESHOLD, sound_objects),
	]

	all_instruments = left_instruments + right_instruments

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

	print("-----READY-----")
	while True:
		serial_data_one = ser1.get_serial()
		serial_data_two = ser2.get_serial()

		for data in (serial_data_one, serial_data_two):
			if data:
				for cur_instrument, value in data.items():
					if value >= cur_instrument.threshold or value == CAPACITANCE_OVERFLOW:
						# check for modulations
						if time.time() - last_modulation_time > MODULATION_COOLDOWN_PERIOD:
							old_key = current_key
							current_key = sound_objects["key"][cur_instrument.name]
							if old_key != current_key:
								modulate(old_key, current_key, all_instruments, cur_instrument)
								last_modulation_time = time.time()
						# play the sound for the key pressed
						cur_instrument.play(current_key)
					else:
						cur_instrument.stop()


		clock.tick(TICKS_PER_SECOND * 3)  # Frame rate in pygame


if __name__ == '__main__':
	main()