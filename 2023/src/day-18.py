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


# Print the grid
def printGrid():
    bounds = [
        min([int(x.real) for x in grid.keys()]),
        max([int(x.real) for x in grid.keys()]),
        min([int(y.imag) for y in grid.keys()]),
        max([int(y.imag) for y in grid.keys()])
    ]
    for y in range(bounds[2], bounds[3] + 1):
        for x in range(bounds[0], bounds[1] + 1):
            p = complex(x, y)
            if p in grid and grid[p] > 0:
                print("█", end="")
            else:
                print(" ", end="")
        print()


# Get digger to dig following a set of instructions
def processData():
    pos = 0
    grid[pos] += 1
    dig(pos, data)
    printGrid()
    return False


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
