"""sound.py

Wrapper class for pygame sounds
"""

import pygame

class Sound(pygame.mixer.Sound):
    """Wrapper for pygame sounds"""

    def __init__(self, file, name: str, key: str):
        """Create new sound with the given name
        
        Parameters:
            name: the name to be shown in the log
        """
        super().__init__(file)
        self.name = name
        self.key = key
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Sound({self.name}, {self.key})"
