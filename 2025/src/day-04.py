#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

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

    grid = {}
    y = 0
    for line in input_fh:
        x = 0
        line = line.rstrip()
        for char in line:
            grid[x + y * 1j] = char
            x += 1
        y += 1

    bounds.extend([x, y])

    return grid


# Print Grid
def printGrid(grid):
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            print(grid[x + y * 1j], end="")
        print()


# Find adjacent rolls
def getAdjacent(grid: dict, pos: int) -> int:
    rolls = 0

    for i in adj:
        chk = pos + i
        if chk.real >= 0 and chk.real < bounds[0] and chk.imag >= 0 and chk.imag < bounds[1]:
            if grid[chk] == "@":
                rolls += 1

    return rolls


# Remove available rolls
def removeRolls(grid: dict, remove: bool):
    count = 0
    newgrid = grid.copy()

    for pos in grid:
        if grid[pos] == "@":
            if getAdjacent(grid, pos) < 4:
                count += 1
                newgrid[pos] = "."
            else:
                newgrid[pos] = "@"

    if remove:
        return newgrid, count

    return grid, count


# Find how many paper rolls can be accessed
def processData(grid):
    return removeRolls(grid, False)[1]


# Repeat until no more rolls can be accessed
def processMore(grid):
    count = 0
    grid, removed = removeRolls(grid, True)

    while removed != 0:
        count += removed
        grid, removed = removeRolls(grid, True)

    return count


def main():
    grid = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(grid)}")

    # Part 2
    print(f"Part 2: {processMore(grid)}")


if __name__ == "__main__":
    main()
