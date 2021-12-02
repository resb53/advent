#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []

bearing = {
    "forward": 1,
    "up": 1j,
    "down": -1j
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.append(line.strip("\n"))


# For each pass, identify its seat
def followDirections():

    location = 0

    for direction in data:
        (dirn, dist) = direction.split(' ')
        location += int(dist) * bearing[dirn]

    print(f"Range: {location.real}, Depth: {location.imag * -1}")
    print(f"Answer 1: {location.real * location.imag * -1}")


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    followDirections()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
