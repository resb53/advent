#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        for rng in line.split(","):
            data.append(rng.split("-"))


# Check for a pattern indicating an invalid code
def checkInvalid(x):
    a, b = x[:len(x)//2], x[len(x)//2:]

    if a == b:
        return int(x)
    else:
        return 0


# For each pass, identify its seat
def processData():
    sum_invalids = 0

    for rng in data:
        for x in range(int(rng[0]), int(rng[1])+1):
            x = str(x)
            if len(x) % 2 != 1:
                sum_invalids += checkInvalid(x)

    return sum_invalids


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
