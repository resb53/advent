#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

maxes = {'x': 0, 'y': 0}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    grid = {}
    loc = 0j

    for line in input_fh:
        line = line.strip("\n")
        for x in line:
            grid[loc] = x
            loc += 1
        maxes["x"] = int(loc.real)
        loc -= loc.real
        loc += 1j
    maxes["y"] = int(loc.imag)

    return grid


# Iterate through time moving seas cucumbers
def moveFauna(grid):
    moved = 1
    steps = 0

    while moved > 0:
        moved = 0

        # East first
        moved += moveAll(grid, ">")

        # Then South
        moved += moveAll(grid, "v")

        steps += 1

    return steps


def moveAll(grid, x):
    movers = []
    for loc in grid:
        if grid[loc] == x:
            if canMove(grid, loc):
                movers.append(loc)
    updateGrid(grid, movers)
    return len(movers)


def canMove(grid, loc):
    check = wrapGrid(grid, loc)
    if grid[check] == ".":
        return True
    else:
        return False


def wrapGrid(grid, loc):
    dest = -1
    if grid[loc] == ">":
        dest = loc + 1
        if dest.real > maxes["x"] - 1:
            dest -= dest.real
    elif grid[loc] == "v":
        dest = loc + 1j
        if dest.imag > maxes["y"] - 1:
            dest -= dest.imag * 1j
    return dest


def updateGrid(grid, movers):
    for loc in movers:
        dest = wrapGrid(grid, loc)
        grid[dest] = grid[loc]
        grid[loc] = "."


def printGrid(grid):
    for y in range(maxes["y"]):
        for x in range(maxes["x"]):
            print(grid[x + y * 1j], end="")
        print()


def main():
    grid = parseInput(args.input)

    # Part 1
    print(f"Solution to part 1: {moveFauna(grid)}")


if __name__ == "__main__":
    main()
