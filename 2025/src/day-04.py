#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
bounds = []
adj = [
    -1-1j, -1j, 1-1j,
    -1, 1,
    -1+1j, 1j, 1+1j
]


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    for line in input_fh:
        x = 0
        line = line.rstrip()
        for char in line:
            grid[x + y * 1j] = char
            x += 1
        y += 1

    bounds.extend([x, y])


# Find adjacent rolls
def getAdjacent(pos):
    rolls = 0

    for i in adj:
        chk = pos + i
        if chk.real >= 0 and chk.real < bounds[0] and chk.imag >= 0 and chk.imag < bounds[1]:
            if grid[chk] == "@":
                rolls += 1

    return rolls


# Find how many paper rolls can be accessed
def processData():
    count = 0
    for pos in grid:
        if grid[pos] == "@":
            if getAdjacent(pos) < 4:
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
