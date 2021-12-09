#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
lows = []
seen = []
basin = {}


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
            lows.append(pos)
            risk += 1 + grid[pos]

    print(f"Solution to Part 1: {risk}")


# Expand basins from a point
def expandBasin(pos):
    size = 0
    for check in ((pos - 1j), (pos - 1), (pos + 1j), (pos + 1)):
        if check in grid:
            if check not in seen:
                if grid[check] != 9:
                    # print(f"Expanding into {check}...")
                    seen.append(check)
                    size += 1
                    size += expandBasin(check)
    return size


# Find basin sizes for low points
def findBasins():
    # Work back through low points, and expand out. Mark other lows seen to skip.
    for pos in lows:
        if pos not in seen:
            seen.append(pos)
            # print(f"Expanding from {pos}...")
            basin[pos] = 1
            basin[pos] += expandBasin(pos)

    sizes = sorted(basin.values())

    print(f"Solution to Part 2: {sizes[-1] * sizes[-2] * sizes[-3]}")


def main():
    parseInput(args.input)

    # Part 1
    findLows()

    # Part 2
    findBasins()


if __name__ == "__main__":
    main()
