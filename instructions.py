import json

from instrument import Instrument
from constants import *
from sound import Sound

class Instructions:
	"""
	Class to parse the music instructions file into Sound objects
	"""

	def __init__(self):
		"""Creates a mapping of instruments to Sound objects and other 
		information mapping: 
		sound purpose -> instrument name -> 
		sound type -> music key -> Sound/list[Sound]

		sound purpose: normal or pivot
		insturment name: name of instrument
		sound type: hold, impact, or release
		music key: key of the music (e.g. F_harmonic_major)
		Sound: the Sound object

		e.g. 
		"normal" -> "lightL" -> "hold" -> "G_sharp_major" -> [Sound, Sound, ...]
		"""
		# Convert json to dict
		instructions = json.load(open(INSTRUCTION_FILE))
		# Replace file names at the end node of the instructions with Sound 
		# object
		for instrument, sound_types in instructions["normal"]:
			for type, music_keys in sound_types.items():
				for music_key, filename_s in music_keys.items():
					# at end node
					if isinstance(filename_s, list):
						music_keys[music_key] = \
							[Sound(filename) for filename in filename_s]
		self.instructions = instructions
	
	def get_sound(
		self, 
		instrument: Instrument, 
		type: str, 
		music_key: str
	) -> Sound:
		"""
		Get the sound object for the given instrument, type, and music key
		Parameters:
			instrument: the instrument to get the sound for
			type: the type of sound (hold, impact, or release)
			music_key: the key of the music (e.g. F_harmonic_major)
		Returns:
			the Sound object
		"""
		return self.instructions["normal"][instrument.name][type][music_key][0]
	
	def get_music_key(self, instrument: Instrument) -> str:
		"""
		Get the key associated with the given instrument
		Parameters:
			instrument: the instrument to get the key for
		Returns:
			key: key string (e.g. F_harmonic_major)
		"""
		return self.instructions["key"][instrument.name]

	def get_all_music_keys(self, instrument: Instrument) -> list[str]:
		"""
		Get the key associated with the given instrument
		Parameters:
			instrument: the instrument to get the key for
		Returns:
			list of keys: list[string] (e.g. F_harmonic_major)
		"""
		return list(self.instructions["normal"][instrument.name]["hold"].keys())
		
		