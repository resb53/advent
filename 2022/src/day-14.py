#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

walls = set()


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        corners = line.strip("\n").split(" -> ")
        startx, starty = [int(x) for x in corners.pop(0).split(",")]

        while len(corners) > 0:
            endx, endy = [int(x) for x in corners.pop(0).split(",")]

            if startx == endx:
                low = min(starty, endy)
                high = max(starty, endy)
                walls.update([endx + y * 1j for y in range(low, high+1)])

            else:
                low = min(startx, endx)
                high = max(startx, endx)
                walls.update([x + endy * 1j for x in range(low, high+1)])

            startx, starty = endx, endy


# Find where a grain of sand will come to rest
def sandfall(sand, voidy, sands, continuous=False):
    if sand + 1j not in walls and sand + 1j not in sands:
        newsand = sand + 1j
    elif sand - 1 + 1j not in walls and sand - 1 + 1j not in sands:
        newsand = sand - 1 + 1j
    elif sand + 1 + 1j not in walls and sand + 1 + 1j not in sands:
        newsand = sand + 1 + 1j
    else:
        return sand

    if not continuous:
        # Part 1
        if int(newsand.imag) != voidy:
            return sandfall(newsand, voidy, sands)
        else:
            return False
    else:
        # Part 2
        if int(newsand.imag) != voidy:
            return sandfall(newsand, voidy, sands, continuous=True)
        else:
            return sand


# Let sand fall fro 500,0 till it reaches the void
def processData():
    origin = 500 + 0j
    voidy = max([int(y.imag) for y in walls])
    sands = set()

    while sandrest := sandfall(origin, voidy, sands):
        sands.add(sandrest)

    print(f"Part 1: {len(sands)}")


# No void, but a floor instead
def processMore():
    origin = 500 + 0j
    floor = max([int(y.imag) for y in walls]) + 2
    sands = set()

    while sandrest := sandfall(origin, floor, sands, continuous=True):
        if sandrest == origin:
            sands.add(sandrest)
            break
        else:
            sands.add(sandrest)

    print(f"Part 2: {len(sands)}")


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
