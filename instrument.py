"""
instrument.py

Class form of each instrument.
"""

from typing import Optional, List
from sound import Sound


class Instrument:
    """Representation of an instrument

    Attributes:
        name: the string name of this instrument
        threshold: the threshold required for this instrument to play
    """

    def __init__(
        self,
        name: str,
        file_name: str,
        holds: Optional[List[Sound]] = None,
        impacts: Optional[List[Sound]] = None,
        threshold: Optional[int] = None
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
        self.name = name
        self.file_name = file_name

        self._holds = [] if holds is None else holds
        self._impacts = [] if impacts is None else impacts
        self.threshold = 0 if threshold is None else threshold

        self._currently_playing = None
    
    def get_key(self, sounds: List[Sound], key: str) -> Sound:
        """Return the sound in sounds with the given key
        
        Parameters:
            sounds: list of sounds to search through
            key: key to search for (needs to be in the same format as the end
            of a filename, e.g. F_harmonic_major.wav)
        
        Returns:
            Sound with given key. If none found raise ValueNotFound.
        """
        for sound in sounds:
            if sound.key == key:
                return sound
        raise ValueError(f"Key ({key}) not found in {self.name}")

    def play(self, key: str) -> None:
        """Play this instrument's sound at the given key

        Parameters:
            key: the key to play in (needs to be in the same format as the end
            of a filename, e.g. F_harmonic_major.wav)

        If called many times, will simply continue to play the current sound
        """
        if not self._currently_playing:
            hold = self.get_key(self._holds, key)
            impact = self.get_key(self._impacts, key)
            print(f"+ {self.name} playing {hold} and {impact}")
            hold.play(loops=-1)
            impact.play()

            self._currently_playing = hold

    def stop(self) -> None:
        """Stop the instrument's current hold sound"""
        if self._currently_playing is not None:
            print(f"- {self.name} stopping {self._currently_playing}")
            self._currently_playing.stop()
            self._currently_playing = None

    def add_hold(self, sound: Sound) -> None:
        """Add the given sound file to the list of hold sounds"""
        self._holds.append(sound)

    def add_impact(self, sound: Sound) -> None:
        """Add the given sound to the list of impact sounds"""
        self._impacts.append(sound)
    
    def set_volume(self, type: str, volume: float) -> None:
        """Set the volume for all sounds of type.
        
        Parameters:
            type: either "hold" or "impact", the type of sound
            volume: Volume to set, in range [0, 1]
        """
        sounds = None
        if type == "hold":
            sounds = self._holds
        else:
            sounds = self._impacts
        
        for sound in sounds:
            sound.set_volume(volume)

    def __str__(self) -> str:
        return f"Instrument: {self.name}, ({len(self._holds)} holds, " \
               f"{len(self._impacts)} impacts)"

    def __repr__(self) -> str:
        return f"Instrument({self.name},{self._holds},{self._impacts}," \
               f"{self.threshold})"

    def __eq__(self, other) -> bool:
        """Return true if the name of these instruments are equal"""
        if isinstance(other, Instrument):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)
