"""
This program allows for conversions between resistor values and colour bands in both directions.
This program only supports 4-band resistors.
"""

from utils import input_checker, clear_screen
from enum import Enum


class Values(Enum):
    GOLD = -2
    SILVER = -1
    BLACK = 0
    BROWN = 1
    RED = 2
    ORANGE = 3
    YELLOW = 4
    GREEN = 5
    BLUE = 6
    PURPLE = 7
    VIOLET = 7
    GREY = 8
    GRAY = 8
    WHITE = 9


class Tolerances(Enum):
    SILVER = 10
    GOLD = 5
    BROWN = 1
    RED = 2
    GREEN = 0.5
    BLUE = 0.25
    PURPLE = 0.10
    VIOLET = 0.10
    GREY = 0.05
    GRAY = 0.05


def value_to_colour():
    pass


def colour_to_value():
    pass


def resistor_converter():
    while True:
        print("Select an option:\n"
              "1: Value to Colour Bands\n"
              "2: Colour Bands to Value\n"
              "3: Exit")
        program_mode = input_checker(1, 3)
        if program_mode == 1:
            value_to_colour()
        elif program_mode == 2:
            colour_to_value()
        elif program_mode == 3:
            break
        else:
            print(">> Error: Invalid option. Press Enter to try again.")
            clear_screen()


if __name__ == '__main__':
    resistor_converter()
