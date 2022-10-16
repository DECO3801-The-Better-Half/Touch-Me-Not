"""arduino_serial.py

Class to parse the input from the arduino serial.
"""

import serial
from instrument import Instrument
from typing import List, Dict, Optional

BOARD_RATE = 9600


class ArduinoSerial:
    """Class to parse input from serial"""

    def __init__(self, order: List[Instrument], port: str):
        """Set the order of the instruments in serial inputs

        Parameters:
            order: the instrument names, in order of appearance
            port: port name
        """
        # Expected order: (left instrument first, right instruments second)
        # l_lamp, l_flower, l_dragonfly,l_plant2, l_plant1, r_lamp, r_water,
        # r_plant2, r_plant1, r_flower
        self._order = order
        self._port = port
        self._ser = serial.Serial(port, BOARD_RATE, timeout=1)

    def get_serial(self) -> Optional[Dict[Instrument, int]]:
        """Return a dictionary mapping instrument name -> value from serial

        Returns:
            dictionary mapping instruments to instrument values or None if
            serial has nothing to read
        """
        if not self._ser.inWaiting():
            return None

        line = self._ser.readline()
        values = line.decode().strip().split(" ")
        result = {}

        for i in range(len(values)):
            result[self._order[i]] = int(values[i])

        return result
