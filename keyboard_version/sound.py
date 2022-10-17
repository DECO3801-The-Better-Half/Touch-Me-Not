"""sound.py

Wrapper class for pygame sounds
"""

import pygame

AUDIO_DIRECTORY = "../audio"

class Sound(pygame.mixer.Sound):
    """Wrapper for pygame sounds"""

    def __init__(self, filename: str):
        """Create new sound with the given name

        Parameters:
            name: the name to be shown in the log
        """
        super().__init__(f"{AUDIO_DIRECTORY}/{filename}")
        self.name = filename.removesuffix(".wav")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Sound({self.name})"
