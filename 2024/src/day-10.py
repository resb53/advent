#!/usr/bin/env python3

import argparse
import sys
from collections import Counter

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
maxv = []
theads = {}
moves = [1, 1j, -1, -1j]


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    for line in input_fh:
        for x, val in enumerate(line.rstrip()):
            grid[x + 1j * y] = int(val)
            if val == "0":
                theads[x + 1j * y] = 0
        y += 1
    maxv.extend([x+1, y])


# For each trailhead, identify how many summits can be reached
def processData():
    total = 0
    for start in theads:
        summits = Counter()
        follow(start, summits)
        total += len(summits)
    return total


# Recursively follow the trail
def follow(pos, peaks):
    height = grid[pos]
    if height == 9:
        peaks[pos] += 1
        return

    for option in moves:
        option += pos
        if option in grid and grid[option] == height + 1:
            follow(option, peaks)


# Print the grid
def printGrid():
    for y in range(maxv[1]):
        for x in range(maxv[0]):
            print(grid[x + 1j * y], end="")
        print()


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
