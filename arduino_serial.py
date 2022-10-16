"""arduino_serial.py

Class to parse the input from the arduino serial.
"""

from typing import List, Dict


class ArduinoSerial:
    """Class to parse input from serial"""

    def __init__(self, order: List[str]):
        """Set the order of the instruments in serial inputs

        Parameters:
            order: the instrument names, in order of appearance
        """
        # Expected order: (left instrument first, right instruments second)
        # l_lamp, l_flower, l_dragonfly,l_plant2, l_plant1, r_lamp, r_water,
        # r_plant2, r_plant1, r_flower
        self._order = order

    def parse_serial(self, serial: bytes) -> Dict[str, int]:
        """Return a dictionary mapping instrument name -> value

        Parameters:
            serial: serial input from the arduino

        Returns:
            dictionary mapping instrument names to values
        """
        values = serial.decode().strip().split(" ")
        result = {}

        for i in range(len(values)):
            result[self._order[i]] = int(values[i])

        return result
