#!/usr/bin/python3

import argparse
import sys
from functools import reduce

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Toboggan Path.")
parser.add_argument('input', metavar='input', type=str,
                    help='Password list input.')
args = parser.parse_args()

grid = {}
xmax = 0
ymax = 0


def main():
    parseInput(args.input)

    # Part 1
    print("Part 1: " + str(findTrees(3 + 1j)))

    # Part 2
    trees = []

    for route in (1 + 1j, 3 + 1j, 5 + 1j, 7 + 1j, 1 + 2j):
        trees.append(findTrees(route))

    print("Part 2: " + str(reduce((lambda x, y: x * y), trees)))

    # Debug
    # printGrid()


# Parse the input file
def parseInput(inp):
    global grid, xmax, ymax
    try:
        grid_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    xcur = 0
    ycur = 0

    for line in grid_fh:
        line = line.strip("\n")
        # parse line and add to dict, with complex key
        # (real on x axis, imag on y)
        xcur = 0

        for element in line:
            grid[xcur + ycur * 1j] = element
            xcur = xcur + 1

        ycur = ycur + 1

    xmax = xcur
    ymax = ycur


# Find the trees on a given slope
def findTrees(slope):
    pos = 0
    trees = 0

    while pos.imag < ymax:
        # Check for need to wrap
        if pos.real >= xmax:
            pos = pos - xmax

        # Check for tree
        if grid[pos] == '#':
            trees = trees + 1

        pos = pos + slope

    return trees


# Print grid
def printGrid():
    for y in range(ymax):
        for x in range(xmax):
            print(grid[x + y * 1j], end='')
        print('')


if __name__ == "__main__":
    main()
