"""main.py

Run this file to read serial input from arduinos and turn it into audio.

The port numbers PORT_ONE and PORT_TWO will likely have to be changed to
the ports that each arduino is attached to.
"""
import pygame
import json
import time
import sys

from instrument import Instrument
from arduino_serial import ArduinoSerial
from modulate import Modulator
from constants import *
from instructions import Instructions

def main():
	"""Run the main loop"""

	# Settings determined by command line arguments
	use_keyboard = False
	use_modulation = False
	port_one = DEFAULT_PORT_ONE
	port_two = DEFAULT_PORT_TWO
	modulation_cooldown_period = None

	# Collect existing users' port settings
	users = {}
	try:
		users = json.load(open(USERS_FILE))
	except FileNotFoundError:
		json.dumps(users, open(USERS_FILE, "w"))

	# Handle command line arguments - see README.md for details
	if len(sys.argv) > 1:
		skip_iteration = False
		username_already_found = False
		for i, arg in enumerate(sys.argv[1:]):
			if skip_iteration:
				skip_iteration = False
				continue
			if arg.startswith("-"):
				if "h" in arg:
					print("Usage: ")
					exit(0)
				if "k" in arg:
					use_keyboard = True
					print("Using keyboard")
				if "m" in arg:
					use_modulation = True
					print("Using modulation")
					try:
						modulation_cooldown_period = int(sys.argv[i + 2])
						skip_iteration = True
					except:
						print(USAGE)
						exit(1)
			else:
				if username_already_found:
					print(USAGE)
					exit(1)
				username_already_found = True
				if arg.lower() in users:
					# Update current port settings
					port_one = users[arg]["port_one"]
					port_two = users[arg]["port_two"]
				else:
					create_new_user = input(f"User {arg} not found. Create new user? (y/n): ")
					if create_new_user.lower() == "y":
						# Create new user
						port_one = input("Enter port for first arduino: e.g. \"/dev/cu.usbserial-10\": ")
						port_two = input("Enter port for second arduino: e.g. \"/dev/cu.usbmodem1101\": ")
						users[arg.lower()] = {"port_one": port_one, "port_two": port_two}
						# Update current port settings
						port_one = users[arg]["port_one"]
						port_two = users[arg]["port_two"]
						# Update users' port setting file
						users_file = open(USERS_FILE, "w")
						json.dump(users, users_file)
						users_file.close()
					else:
						print("Exiting...")
						exit(0)

	# Initialise pygame and Sound objects
	print("Initialising...")
	pygame.init()

	if use_keyboard:
		(width, height) = (300, 200)
		screen = pygame.display.set_mode((width, height))
		pygame.display.flip()


	current_key = "G_sharp_major"
	last_modulation_time = time.time()
	instructions = Instructions()

	# Initialise our instruments in the right order so ArduinoSerial can read them
	left_instruments = [
		Instrument("Left lamp", "lightL", BASE_THRESHOLD, instructions),
		Instrument("Left flower", "flowerL", BASE_THRESHOLD, instructions),
		Instrument("Dragonfly", "dragonfly", BASE_THRESHOLD, instructions),
		Instrument("Left plant 2", "plantFL", BASE_THRESHOLD, instructions),
		Instrument("Left plant 1", "plantL", BASE_THRESHOLD, instructions),
	]

	right_instruments = [
		Instrument("Right lamp", "lightR", BASE_THRESHOLD, instructions),
		Instrument("Water", "water", BASE_THRESHOLD + 200, instructions),
		Instrument("Right plant 2", "plantFR", BASE_THRESHOLD, instructions),
		Instrument("Right plant 1", "plantR", BASE_THRESHOLD, instructions),
		Instrument("Right flower", "flowerR", BASE_THRESHOLD, instructions),
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

	ser1 = None
	ser2 = None
	if not use_keyboard:
		# Initialise arduinos
		ser1 = ArduinoSerial(left_instruments, port_one)
		ser2 = ArduinoSerial(right_instruments, port_two)

	print("-----READY-----")
	# Main loop
	while True:
		if not use_keyboard:
			# Read from arduino
			serial_data_one = ser1.get_serial()
			serial_data_two = ser2.get_serial()
			for data in (serial_data_one, serial_data_two):
				if data:
					for cur_instrument, value in data.items():
						if value >= cur_instrument.threshold or value == CAPACITANCE_OVERFLOW:
							# Instrument is being touched
							# Check for modulations
							if use_modulation and time.time() - last_modulation_time > modulation_cooldown_period:
								old_key = current_key
								current_key = instructions.get_music_key(cur_instrument)
								if old_key != current_key:
									# Modulate
									Modulator.modulate(old_key, current_key, all_instruments, cur_instrument)
									last_modulation_time = time.time()
							# Play the sound for the key pressed
							cur_instrument.play(current_key)
						else:
							# Instrument is not being touched
							cur_instrument.stop()
		else:
			# Read from keyboard
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				elif event.type == pygame.KEYDOWN:
					number_pressed = event.key - 48
					if number_pressed in range(0, 10):
						# Instrument is being touched
						# Check for modulations
						if use_modulation and time.time() - last_modulation_time > modulation_cooldown_period:
							old_key = current_key
							current_key = instructions.get_music_key(all_instruments[number_pressed])
							if old_key != current_key:
								Modulator.modulate(old_key, current_key, all_instruments, all_instruments[number_pressed])
								last_modulation_time = time.time()
						# Play the sound for the key pressed
						all_instruments[number_pressed].play(current_key)
				elif event.type == pygame.KEYUP:
					number_pressed = event.key - 48
					if number_pressed in range(0, 10):
						all_instruments[number_pressed].stop()
		clock.tick(TICKS_PER_SECOND * 3)  # Frame rate in pygame


if __name__ == '__main__':
	main()
