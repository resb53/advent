#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

bounds = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    grid = {}
    y = 0

    for line in input_fh:
        x = 0
        line = line.rstrip()
        for char in line:
            if char == ".":
                grid[x + y * 1j] = 0
            else:
                grid[x + y * 1j] = char
            x += 1
        y += 1

    bounds.extend([x, y])

    return grid


# Print Grid
def printGrid(grid):
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            if grid[x + y * 1j] == 0:
                print(".", end="")
            else:
                print(grid[x + y * 1j], end="")
        print()


# Pass Tachyon beams through the field
def processData(g):
    grid = g.copy()
    split = 0

    for y in range(1, bounds[1]):
        for x in range(bounds[0]):
            if grid[x + y * 1j] == 0 and grid[x + (y-1) * 1j] in ["S", 1]:
                grid[x + y * 1j] = 1
            if grid[x + y * 1j] == "^" and grid[x + (y-1) * 1j] == 1:
                split += 1
                grid[x-1 + y * 1j] = 1
                grid[x+1 + y * 1j] = 1

    return split


# Count Tachyon beam paths through the field
def processMore(g):
    grid = g.copy()

    for y in range(1, bounds[1]):
        for x in range(bounds[0]):
            if grid[x + y * 1j] != "^":
                if grid[x + y * 1j] >= 0:
                    if grid[x + (y-1) * 1j] == "S":
                        grid[x + y * 1j] = 1
                    elif grid[x + (y-1) * 1j] != "^" and grid[x + (y-1) * 1j] > 0:
                        grid[x + y * 1j] += grid[x + (y-1) * 1j]
            elif grid[x + y * 1j] == "^":
                if grid[x + (y-1) * 1j] > 0:
                    grid[x-1 + y * 1j] += grid[x + (y-1) * 1j]
                    grid[x+1 + y * 1j] += grid[x + (y-1) * 1j]

    routes = 0
    for x in range(bounds[0]):
        routes += grid[x + (bounds[1] - 1) * 1j]

    return routes


def main():
    grid = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(grid)}")

    # Part 2
    print(f"Part 2: {processMore(grid)}")


if __name__ == "__main__":
    main()
