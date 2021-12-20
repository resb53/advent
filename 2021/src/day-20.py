#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

lookup = {}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    line = input_fh.readline().strip("\n")
    k = 0
    for v in line:
        if v == "#":
            lookup[k] = 1
        else:
            lookup[k] = 0
        k += 1

    _ = input_fh.readline()

    grid = defaultdict(int)
    loc = 0j

    for line in input_fh:
        line = line.strip("\n")
        for x in line:
            if x == '#':
                grid[loc] = 1
            else:
                grid[loc] = 0
            loc += 1
        loc -= loc.real
        loc += 1j

    return grid


# Move through entire image enhancing values
def enhanceImage(grid, infspace):
    newgrid = defaultdict(int)

    (minx, maxx, miny, maxy) = getBounds(grid)

    # Add 2 rings of infinitespace, calculate using one of them, return grid and that 1
    for y in (miny - 2, miny - 1, maxy + 1, maxy + 2):
        for x in range(minx - 2, maxx + 3):
            grid[x + y * 1j] = infspace
    for x in (minx - 2, minx - 1, maxx + 1, maxx + 2):
        for y in range(miny, maxy + 1):
            grid[x + y * 1j] = infspace

    # printGrid(grid)

    for y in range(miny - 1, maxy + 2):
        for x in range(minx - 1, maxx + 2):
            pos = x + y * 1j
            newgrid[pos] = enhanceValue(grid, pos)

    infspace = lookup[int(str(infspace) * 9, 2)]

    return (newgrid, infspace)


def getBounds(grid):
    locs = list(grid.keys())

    (minx, maxx, miny, maxy) = (0, 0, 0, 0)

    for pos in locs:
        if pos.real < minx:
            minx = int(pos.real)
        if pos.real > maxx:
            maxx = int(pos.real)
        if pos.imag < miny:
            miny = int(pos.imag)
        if pos.imag > maxy:
            maxy = int(pos.imag)

    return (minx, maxx, miny, maxy)


# Enhave given value in image
def enhanceValue(grid, pos):
    niner = ""
    for x in [-1-1j, 0-1j, 1-1j, -1, 0, 1, -1+1j, 0+1j, 1+1j]:
        niner += str(grid[pos + x])
    return lookup[int(niner, 2)]


def printGrid(grid):
    (minx, maxx, miny, maxy) = getBounds(grid)

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            pos = x + y * 1j
            print(grid[pos], end="")
        print("")


def main():
    grid = parseInput(args.input)
    infspace = 0

    # Part 1
    for _ in range(50):
        (grid, infspace) = enhanceImage(grid, infspace)

    print(f"Solution to part 1: {sum(grid.values())}")


if __name__ == "__main__":
    main()
