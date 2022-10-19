"""constants.py

stores all constants for all components of the player system
"""

INSTRUCTION_FILE = "instructions.json"
USERS_FILE = "user_port_settings.json"
AUDIO_DIRECTORY = "../audio"
TICKS_PER_SECOND = 30
BASE_THRESHOLD = 800
DEFAULT_PORT_ONE = '/dev/cu.usbserial-10'
DEFAULT_PORT_TWO = '/dev/cu.usbmodem1101'
CAPACITANCE_OVERFLOW = -2
NUM_AUDIO_CHANNELS = 20

USAGE = """
Usage: python3 main.py [username] [-m cooldown] [-k]
	username: name of new or existing user
		(used to select port names)
	-m cooldown: use modulation mode with modulation cooldown period in seconds
		(changes musical key when an object is touch after cooldown period)
	-k: use keyboard keys 0-9 to represent object touches instead of Arduino input
		(may not work on systems with incompatible key mappings)
(see README.md for details)
"""
