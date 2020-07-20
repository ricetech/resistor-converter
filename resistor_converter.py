"""
This program allows for conversions between resistor values and color bands in both directions.
This program only supports 4-band and 5-band resistors.
"""

from utils import input_checker, clear_screen
from enum import Enum
# noinspection PyUnresolvedReferences
from typing import Union
import math
from decimal import Decimal


class Values(Enum):
    SILVER = -2
    GOLD = -1
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


def round_to_n(x, n):
    if not x:
        return 0
    power = -int(math.floor(math.log10(abs(x)))) + (n - 1)
    factor = (10 ** power)
    return round(x * factor) / factor


def not_quite_scientific_notation(x):
    s = "{:.2E}".format(Decimal(round_to_n(x, 3)))
    v = s.split("E")
    a = int(float(v[0]) * 100)
    b = int(v[1])-2
    return a, b


def value_to_color():
    pass


def color_to_value(colors):
    """
    This function will take a list containing the color bands of a 4 or 5 band resistor in order and then
    calculate the resistance and tolerance of that resistor.
    The provided list parameter will NOT be modified.
    :param colors: A list containing the color bands of the resistor in order from left to right
    :type colors: list of str
    :return: The resistance and tolerance of the resistor provided.
    :rtype: (Union[int, float], Union[int, float])
    :raises ValueError: If the resistor provided contains an invalid number of bands (len(colors) != 4 or 5 bands),
    or if any of the provided colors are invalid.
    """
    bands = []

    # Add all of the numerical bands including the multiplier band
    # Ignoring the last value (len(colors) - 1) since that's the tolerance band to be calculated later
    for i in range(len(colors) - 1):
        try:
            color = colors[i].upper()
            bands.append(Values[color].value)
        except KeyError:
            # noinspection PyUnboundLocalVariable
            error_message = "Color in band " + str(i + 1) + " is not a valid resistor band color: " + color
            raise ValueError(error_message) from None

    # Find the first occurrences of gold and silver to check later
    try:
        first_gold = bands.index(-1)
    except ValueError:
        # Use random large value that will satisfy the condition when checking for the first occurrence
        first_gold = 99
    try:
        first_silver = bands.index(-2)
    except ValueError:
        first_silver = 99

    # Look up and store the tolerance (Always the last band for 4 and 5 band resistors)
    try:
        tolerance = Tolerances[colors[len(colors) - 1].upper()].value
    except KeyError:
        error_message = "Color is not a valid color for the tolerance band: " + colors[len(colors) - 1]
        raise ValueError(error_message) from None

    # Calculate resistor value
    # 4-band resistors (len = 3 because we don't add the last band to bands)
    if len(bands) == 3:
        # Raise Error if gold or silver is found in an invalid band
        if first_gold < 2:
            raise ValueError("Gold is only valid in Band 3 or 4. Found 'gold' in band " + str(first_gold + 1) + ".")
        elif first_silver < 2:
            raise ValueError("Silver is only valid in Band 3 or 4. "
                             "Found 'silver' in band " + str(first_silver + 1) + ".")

        resistance = 10 * bands[0] + bands[1]
    # 5-band resistors (len = 4 because we don't add the last band to bands)
    elif len(bands) == 4:
        # Raise Error if gold or silver is found in an invalid band
        if first_gold < 2:
            raise ValueError("Gold is only valid in Band 4 or 5. Found 'gold' in band " + str(first_gold + 1) + ".")
        elif first_silver < 2:
            raise ValueError("Silver is only valid in Band 4 or 5."
                             " Found 'silver' in band " + str(first_silver + 1) + ".")

        resistance = 100 * bands[0] + 10 * bands[1] + bands[2]
    else:
        error_message = "Unsupported number of bands. Only 4 and 5 band resistors are supported."
        raise ValueError(error_message)

    # Multiply by the multiplier band (Always the 2nd last band for 4 and 5 band resistors)
    resistance *= 10 ** bands[len(bands) - 1]

    return resistance, tolerance


def value_to_color_human():
    pass


def color_to_value_human():
    done = False
    clear_screen()
    print("Color Band to Value Converter\n"
          ">> Note: When entering colors in this program, the capitalization of the color doesn't matter.")

    while not done:
        while True:
            try:
                bands_input = input("Enter the colors of the resistor bands from left to right separated by spaces:\n")
                bands = bands_input.split(' ')
                if len(bands) == 4 or len(bands) == 5:
                    # Calculate resistor value
                    resistance, tolerance = color_to_value(bands)

                    # Account for large units
                    if resistance > 999999999:
                        resistance //= 1000000000
                        units = " GΩ (x10^9 Ω)"
                    elif resistance > 999999:
                        resistance //= 1000000
                        units = " MΩ (x10^6 Ω)"
                    elif resistance > 999:
                        resistance //= 1000
                        units = " KΩ (x10^3 Ω)"
                    else:
                        units = " Ω"

                    # Print resistor value and tolerance
                    print("\nResistor value and tolerance:\n" + str(resistance) + units + " ± " + str(tolerance) + " Ω")
                    break
                else:
                    print(">> Error: This program only supports 4 and 5-band resistors. You provided",
                          len(bands), "band(s):", ', '.join(bands))
                    input("Press Enter to try again. ")
                    clear_screen()

            # Catch and display any errors raised by color_to_value()
            except ValueError as e:
                print(">> Error:", str(e))
                input("Press Enter to try again. ")
                clear_screen()

        # Prompt to convert another resistor
        print()
        while True:
            repeat_input = input("Convert another resistor? (Y/N): ")
            if repeat_input.upper() == "Y":
                clear_screen()
                break
            elif repeat_input.upper() == "N":
                done = True
                break
            else:
                print(">> Error: Not an option. Enter Y or N.")
                input("Press Enter to try again. ")
                clear_screen()


def resistor_converter():
    while True:
        print("Select an option:\n"
              "1: Value to color Bands\n"
              "2: color Bands to Value\n"
              "3: Exit")
        program_mode = input_checker(1, 3)
        if program_mode == 1:
            print(">> Error: This function is not available yet.")
            input("Press Enter to try again. ")
            clear_screen()
        elif program_mode == 2:
            color_to_value_human()
            clear_screen()
        elif program_mode == 3:
            break
        else:
            print(">> Error: Invalid option. Press Enter to try again. ")
            clear_screen()


if __name__ == '__main__':
    x = 1
    y = not_quite_scientific_notation(x)
    print(y)
    resistor_converter()
