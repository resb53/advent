#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict
from itertools import combinations

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
antennas = defaultdict(list)
antinodes = defaultdict(set)
harmonics = defaultdict(set)
maxv = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    for line in input_fh:
        for x, val in enumerate(line.rstrip()):
            grid[x + 1j * y] = val
            if val != ".":
                antennas[val].append(x + 1j * y)
        y += 1
    maxv.extend([x + 1, y])


# Inspect the grid
def printGrid():
    for y in range(maxv[1]):
        for x in range(maxv[0]):
            if (x + 1j * y) in antinodes:
                print("#", end="")
            else:
                print(grid[x + 1j * y], end="")
        print()


# For each frequency find its antinodes
def processData():
    for freq in antennas:
        for pair in combinations(antennas[freq], 2):
            diff = pair[0] - pair[1]
            anode = [pair[0] + diff, pair[1] - diff]
            for x in anode:
                if x in grid:
                    antinodes[x].add(freq)
    return len(antinodes)


# Antinodes for all aligned points
def processMore():
    for freq in antennas:
        for pair in combinations(antennas[freq], 2):
            diff = pair[0] - pair[1]
            loc = pair[0]
            while loc in grid:
                harmonics[loc].add(freq)
                loc += diff
            loc = pair[1]
            while loc in grid:
                harmonics[loc].add(freq)
                loc -= diff
    return len(harmonics)


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
