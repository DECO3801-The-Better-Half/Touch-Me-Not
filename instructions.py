import json
from sound import Sound

from constants import *

class Instructions:
	"""
	Static class to parse the music instructions file into Sound objects
	"""
	
	def get_audio() -> dict[str, dict[str, dict[str, dict[str, list[Sound]]]]]:
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
		return instructions