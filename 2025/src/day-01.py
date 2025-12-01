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
        dir = line[0]
        dist = int(line[1:])
        data.append([dir, dist])


# For each pass, identify its seat
def processData():
    dial = 50
    count = 0

    for instr in data:
        if instr[0] == "R":
            dial = (dial + instr[1]) % 100
        else:
            dial = (dial - instr[1]) % 100

        if dial == 0:
            count += 1

    return count


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
