#!/usr/bin/python3

import argparse
import sys
import re

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Bitmask.")
parser.add_argument('input', metavar='input', type=str,
                    help='Bitwise data input.')
args = parser.parse_args()

data = {}


class bit36:
    'Class for 36 bit unsigned integers'
    value = 0
    bits = [0] * 36  # Most significant to least significant

    def __init__(self, val):
        if not isinstance(val, int):
            raise TypeError("Must be passed integer value.")
        if val < 0 or val > 68719476735:
            raise ValueError('Value initiated is outside bounds of 36-bit int.')

        self.value = val
        for i, v in enumerate('{0:036b}'.format(val)):
            self.bits[i] = v

    def __repr__(self):
        return str(self.value)


def main():
    parseInput(args.input)

    # Part 1
    findInit()

    # Part 2

    # Debug
    printData()


# Parse the input file
def parseInput(inp):
    global data
    mask = ''
    try:
        data_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in data_fh:
        match = re.match(r"^mem\[(\d+)\] = (\d+)$", line, re.I)
        if not match:
            mask = line.split(" = ")[1]
            print(f"New mask: {mask}")
        else:
            data[bit36(int(match.group(1)))] = bit36(int(match.group(2)))


# For each pass, identify its seat
def findInit():
    return True


def printData():
    for mem in data:
        print(f"{mem}: {data[mem]}")


if __name__ == "__main__":
    main()
