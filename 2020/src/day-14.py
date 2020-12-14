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
    def __init__(self, val):
        if not isinstance(val, int):
            raise TypeError("Must be passed integer value.")
        if val < 0 or val > 68719476735:
            raise ValueError('Value initiated is outside bounds of 36-bit int.')

        self.bits = [0] * 36  # Most significant to least significant
        for i, v in enumerate('{0:036b}'.format(val)):
            self.bits[i] = v

    def setbit(self, i, v):
        self.bits[i] = v

    def __int__(self):
        return int(''.join(self.bits), 2)

    def __radd__(self, other):
        return other + int(self)

    def __repr__(self):
        return str(int(self))


def main():
    parseInput(args.input)

    # Part 1
    print(findInit())

    # Part 2

    # Debug
    # printData()


# Parse the input file
def parseInput(inp):
    global data
    mask = ['X'] * 36
    try:
        data_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in data_fh:
        match = re.match(r"^mem\[(\d+)\] = (\d+)$", line, re.I)
        if not match:
            mask = list(line.strip("\n").split(" = ")[1])
        else:
            mem = bit36(int(match.group(1)))
            val = bit36(int(match.group(2)))

            # Apply mask to val
            for i, v in enumerate(mask):
                if v != 'X':
                    val.setbit(i, v)

            data[int(mem)] = val


# For each pass, identify its seat
def findInit():
    return sum(data.values())


def printData():
    for mem in data:
        print(f"{mem}: {data[mem]}")


if __name__ == "__main__":
    main()
