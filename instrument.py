"""
instrument.py

Class form of each instrument.
"""

import pygame
from typing import Optional, List


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
        holds: Optional[List[pygame.mixer.Sound]] = None,
        impacts: Optional[List[pygame.mixer.Sound]] = None,
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

    def play(self) -> None:
        """Play this instrument's sound

        If called many times, will simply continue to play the current sound
        """
        if not self._currently_playing:
            self._holds[0].play(loops=-1)
            self._impacts[0].play()

            self._currently_playing = self._holds[0]

    def stop(self) -> None:
        """Stop the instrument's current hold sound"""
        if self._currently_playing is not None:
            self._currently_playing.stop()
            self._currently_playing = None

    def add_hold(self, sound: pygame.mixer.Sound) -> None:
        """Add the given sound file to the list of hold sounds"""
        self._holds.append(sound)

    def add_impact(self, sound: pygame.mixer.Sound) -> None:
        """Add the given sound to the list of impact sounds"""
        self._impacts.append(sound)

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
