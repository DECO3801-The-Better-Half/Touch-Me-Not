"""
instrument.py

Class form of each instrument.
"""

import pygame


class Instrument:
    """Representation of an instrument

    Attributes:
        name: the string name of this instrument
        threshold: the threshold required for this instrument to play
    """

    def __init__(
        self,
        name: str,
        holds: list[pygame.mixer.Sound],
        impacts: list[pygame.mixer.Sound],
        threshold: int
    ) -> None:
        """Create an instrument

        Parameter:
            name: the name of the instrument (e.g. L plant1)
            holds: list of the sounds to play while the instrument is
                held (can be only one sound)
            impacts: list of the sounds to play when the instrument is
                pressed (can be only one sound)
            threshold: threshold for arduino output
        """
        self.name = name
        self._holds = holds
        self._impacts = impacts
        self.threshold = threshold

        self._currently_playing = None

    def play(self) -> None:
        """Play this instrument's sound"""
        self._holds[0].play(loops=-1)
        self._impacts[0].play()

        self._currently_playing = self._holds[0]

    def stop(self) -> None:
        """Stop the instrument's current hold sound"""
        if self._currently_playing is not None:
            self._currently_playing.stop()

    def __eq__(self, other) -> bool:
        """Return true if the name of these instruments are equal"""
        if isinstance(other, Instrument):
            return self.name == other.name
        return False
