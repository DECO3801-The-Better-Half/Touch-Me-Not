"""
instrument.py

Class form of each instrument and teh instructions of each instrument
"""
from __future__ import annotations
import json
from constants import INSTRUCTION_FILE
from sound import Sound


class Instrument:
    """Representation of an instrument

    Attributes:
        readable_name: the readable name of this instrument
        name: the name of this instrument according to the audio files
        threshold: the threshold required for this instrument to play
        instructions: instructions to play this instrument
    """

    def __init__(
            self,
            readable_name: str,
            name: str,
            threshold: int,
            instructions: Instructions
    ) -> None:
        """Create an instrument

        Parameter:
            readable_name: the name to be shown in the log
            name: the name of the instrument
            threshold: the threshold required for this instrument to play
            instructions: the instructions to play this instrument
        """
        self.readable_name = readable_name
        self.name = name
        self.threshold = 0 if threshold is None else threshold
        self.instructions = instructions

        self._currently_playing = None

    def play(self, music_key: str, play_impact: bool = True) -> None:
        """Play this instrument's sound at the given key

        Parameters:
            music_key: the key to play in (needs to be in the same format as the
                end of a filename, e.g. F_harmonic_major.wav)
            play_impact: True if the impact sound should be played

        If called many times, will simply continue to play the current sound
        """
        if not self._currently_playing:
            hold = self.instructions.get_sound(self, "hold", music_key)
            impact = self.instructions.get_sound(self, "impact", music_key)
            print(f"+ {self.readable_name} playing {hold}")
            hold.play(loops=-1)
            if play_impact:
                print(f"+ {self.readable_name} playing {impact}")
                impact.play()
            self._currently_playing = hold

    def stop(self) -> None:
        """Stop the instrument's current hold sound"""
        if self._currently_playing is not None:
            print(f"- {self.readable_name} stopping {self._currently_playing}")
            self._currently_playing.stop()
            self._currently_playing = None

    def set_volume(self, music_type: str, volume: float) -> None:
        """Set the volume for all sounds of type.

        Parameters:
            music_type: either "hold" or "impact", the type of sound
            volume: Volume to set, in range [0, 1]
        """
        for music_key in self.instructions.get_all_music_keys(self):
            self.instructions.get_sound(self, music_type, music_key) \
                .set_volume(volume)

    def __str__(self) -> str:
        return f"Instrument: {self.readable_name})"

    def __repr__(self) -> str:
        return f"Instrument({self.readable_name},{self.threshold}," \
               f"{self.instructions},{self.threshold})"

    def __eq__(self, other) -> bool:
        """Return true if the name of these instruments are equal"""
        if isinstance(other, Instrument):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)


class Instructions:
    """
    Class to parse the music instructions file into Sound objects
    """

    def __init__(self):
        """Creates a mapping of instruments to Sound objects and other
        information mapping:
        sound purpose -> instrument name ->
        sound music_type -> music key -> Sound/list[Sound]

        sound purpose: normal or pivot
        insturment name: name of instrument
        sound music_type: hold, impact, or release
        music key: key of the music (e.g. F_harmonic_major)
        Sound: the Sound object

        e.g.
        "normal" -> "lightL" -> "hold" -> "G_sharp_major" -> [Sound, Sound, ...]
        """
        # Convert json to dict
        instructions = json.load(open(INSTRUCTION_FILE))
        # Replace file names at the end node of the instructions with Sound
        # object
        for _, sound_types in instructions["normal"].items():
            for _, music_keys in sound_types.items():
                for music_key, filename_s in music_keys.items():
                    # at end node
                    if isinstance(filename_s, list):
                        music_keys[music_key] = \
                            [Sound(filename) for filename in filename_s]
        self.instructions = instructions

    def get_sound(
            self,
            instrument: Instrument,
            music_type: str,
            music_key: str
    ) -> Sound:
        """
        Get the sound object for the given instrument, type, and music key
        Parameters:
            instrument: the instrument to get the sound for
            music_type: the type of sound (hold, impact, or release)
            music_key: the key of the music (e.g. F_harmonic_major)
        Returns:
            the Sound object
        """
        return self.instructions["normal"][instrument.name][music_type] \
            [music_key][0]

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
