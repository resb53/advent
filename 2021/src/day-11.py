#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    loc = 0j

    for line in input_fh:
        line = line.strip("\n")
        for x in line:
            grid[loc] = int(x)
            loc += 1
        loc -= loc.real
        loc += 1j


# For each pass, identify its seat
def buildCharge():
    # First, the energy level of each octopus increases by 1.
    for pos in grid:
        grid[pos] += 1

    # Then, any octopus with an energy level greater than 9 flashes.
    count = 0
    flashed = []

    for pos in grid:
        if grid[pos] > 9 and pos not in flashed:
            count += flash(pos, flashed)

    # Finally, any octopus that flashed during this step has its energy level set to 0.
    for pos in flashed:
        grid[pos] = 0

    return count


# Enact octopus flash
def flash(pos, flashed):
    countall = 1
    flashed.append(pos)
    for x in (pos - 1 - 1j, pos - 1j, pos + 1 - 1j,
              pos - 1,               pos + 1,
              pos - 1 + 1j, pos + 1j, pos + 1 + 1j):
        if x in grid:
            grid[x] += 1
            if grid[x] > 9 and x not in flashed:
                countall += flash(x, flashed)
    return countall


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    flashes = 0
    for _ in range(100):
        flashes += buildCharge()
    print(f"Solution to part 1: {flashes}")

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
