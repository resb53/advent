#!/usr/bin/python3

import argparse
import sys
import cmath

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Toboggan Path.")
parser.add_argument('input', metavar='input', type=str, help='Password list input.')
args = parser.parse_args()

grid = {}
xmax = 0
ymax = 0


def main():
    parseInput(args.input)
    findTrees()

# Parse the input file
def parseInput(inp):
    global grid, xmax, ymax
    try:
        grid_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    xcur = 0
    ycur = -1

    for line in grid_fh:
        line = line.strip("\n")
        # parse line and add to dict, with complex key (real on x axis, imag on y)
        xcur = 0
        ycur = ycur + 1
        
        for element in line:
            grid[xcur + ycur * 1j] = element
            xcur = xcur + 1

    xmax = xcur
    ymax = ycur


# Find the trees on a given slope
def findTrees():
    pos = 0
    print(str(xmax) + ',' + str(ymax))

    for y in range(ymax):
        for x in range(xmax):
            print(grid[x + y * 1j], end='')
        print('')


if __name__ == "__main__":
    main()
