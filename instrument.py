"""
instrument.py

Class form of each instrument.
"""

from typing import Optional, List, Union
from sound import Sound


class Instrument:
	"""Representation of an instrument

	Attributes:
		name: the string name of this instrument
		threshold: the threshold required for this instrument to play
	"""

	def __init__(
		self,
		readable_name: str,
		name: str,
		threshold: int,
		sound_objects: dict[str, dict[str, dict[str, dict[str, Union[Sound, list[Sound]]]]]]
		# sound_objects: sound purpose -> instrument name -> sound type -> music key -> Sound/list[Sound]
	) -> None:
		"""Create an instrument

		Parameter:
			name: the name of the instrument (e.g. L plant1)
			file_name: the name of this instrument according to the files
			holds: list of the sounds to play while the instrument is
				held (can be only one sound)
			impacts: list of the sounds to play when the instrument is
				pressed (can be only one sound)
			threshold: threshold for arduino output
		"""
		self.readable_name = readable_name
		self.name = name
		self.threshold = 0 if threshold is None else threshold
		self.sound_objects = sound_objects

		self._currently_playing = None

	def play(self, key: str, play_impact: bool = True) -> None:
		"""Play this instrument's sound at the given key

		Parameters:
			key: the key to play in (needs to be in the same format as the end
			of a filename, e.g. F_harmonic_major.wav)

		If called many times, will simply continue to play the current sound
		"""
		if not self._currently_playing:
			hold = self.sound_objects["normal"][self.name]["hold"][key][0]
			impact = self.sound_objects["normal"][self.name]["impact"][key][0]
			print(f"+ {self.name} playing {hold}")
			hold.play(loops=-1)
			if play_impact:
				print(f"+ {self.name} playing {impact}")
				impact.play()

			self._currently_playing = hold

	def stop(self) -> None:
		"""Stop the instrument's current hold sound"""
		if self._currently_playing is not None:
			print(f"- {self.name} stopping {self._currently_playing}")
			self._currently_playing.stop()
			self._currently_playing = None
	
	def set_volume(self, type: str, volume: float) -> None:
		"""Set the volume for all sounds of type.
		
		Parameters:
			type: either "hold" or "impact", the type of sound
			volume: Volume to set, in range [0, 1]
		"""
		# loop over each music key in normal sounds
		for music_key in self.sound_objects["normal"][self.name][type]:
			# loop over each sound
			for sound in self.sound_objects["normal"][self.name][type][music_key]:
				sound.set_volume(volume)

	def __str__(self) -> str:
		return f"Instrument: {self.readable_name}, ({len(self._holds)} holds, " \
			f"{len(self._impacts)} impacts)"

	def __repr__(self) -> str:
		return f"Instrument({self.readable_name},{self._holds},{self._impacts}," \
			f"{self.threshold})"

	def __eq__(self, other) -> bool:
		"""Return true if the name of these instruments are equal"""
		if isinstance(other, Instrument):
			return self.name == other.name
		return False

	def __hash__(self):
		return hash(self.name)
