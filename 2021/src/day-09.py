#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    loc = 0j

    for line in input_fh:
        line = line.strip("\n")
        for x in line:
            grid[loc] = int(x)
            loc += 1
        loc -= loc.real
        loc += 1j


# Find lowest neighbour points
def findLows():
    risk = 0
    for pos in grid:
        low = True
        for check in ((pos - 1j), (pos - 1), (pos + 1j), (pos + 1)):
            if check in grid:
                if grid[check] <= grid[pos]:
                    low = False
        if low:
            risk += 1 + grid[pos]

    print(f"Solution to Part 1: {risk}")


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    findLows()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
