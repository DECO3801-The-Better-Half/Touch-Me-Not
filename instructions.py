import json

from constants import *
from sound import Sound

class Instructions:
	"""
	Class to parse the music instructions file into Sound objects
	"""

	def __init__(self):
		"""Creates a mapping of instruments to Sound objects and other information
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
		self.instructions = instructions
	
	def get_sound(self, instrument: 'Instrument', type: str, music_key: str) -> Sound:
		"""
		Get the sound object for the given instrument, type, and music key
		Returns:
			the Sound object
		"""

		return self.instructions["normal"][instrument.name][type][music_key][0]
	
	def get_music_key(self, instrument: 'Instrument') -> str:
		"""
		Get the key associated with the given instrument
		Returns:
			key: string (e.g. F_harmonic_major)
		"""
		return self.instructions["key"][instrument.name]

	def get_all_music_keys(self, instrument: 'Instrument') -> 'Instrument':
		"""
		Get the key associated with the given instrument
		Returns:
			list of keys: list[string] (e.g. F_harmonic_major)
		"""
		return list(self.instructions["normal"][instrument.name]["hold"].keys())
		
		