#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
grid = defaultdict(int)
compass = {
    "U": -1j,
    "R": 1,
    "D": 1j,
    "L": -1
}
sys.setrecursionlimit(100000)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        vals = line.rstrip().split()
        vals[1] = int(vals[1])
        vals[2] = vals[2].strip("(#)")
        data.append(vals)


# Dig according to the plan
def dig(pos, plan):
    for instr in plan:
        (drn, length, _) = instr
        for _ in range(length):
            pos += compass[drn]
            grid[pos] += 1


# Get boundaries of the grid
def getBounds():
    return [
        min([int(x.real) for x in grid.keys()]),
        max([int(x.real) for x in grid.keys()]),
        min([int(y.imag) for y in grid.keys()]),
        max([int(y.imag) for y in grid.keys()])
    ]


# Dig adjacent undug tiles
def digAround(pos):
    around = []
    for x in [-1j, 1-1j, 1, 1+1j, 1j, -1+1j, -1, -1-1j]:
        if pos + x not in grid:
            around.append(pos + x)
    if len(around) > 0:
        for x in around:
            grid[x] += 1
            digAround(x)


# Fill in the perimeter
def floodFill():
    # Find a start within the perimeter
    bounds = getBounds()
    pointer = None
    for row in range(bounds[2], bounds[3] + 1):
        points = [x for x in grid.keys() if x.imag == row]
        if len(points) == 2:
            points.sort(key=lambda x: x.real)
            pointer = points[0] + 1
            break
    # Get all spaces around the start within the perimeter
    grid[pointer] += 1
    digAround(pointer)


# Print the grid
def printGrid():
    bounds = getBounds()
    for y in range(bounds[2], bounds[3] + 1):
        for x in range(bounds[0], bounds[1] + 1):
            p = complex(x, y)
            if p in grid and grid[p] > 0:
                print(grid[p], end="")
            else:
                print(" ", end="")
        print()


# Get digger to dig following a set of instructions
def processData():
    pos = 0
    grid[pos] += 1
    dig(pos, data)
    floodFill()
    return len(grid.keys())


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
