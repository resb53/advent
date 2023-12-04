#!/usr/bin/env python3

import argparse
import sys
from numpy import prod

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        dataline = []
        line = line.strip("\n").split(": ")[1]
        plays = line.split("; ")

        for play in plays:
            reveal = [0, 0, 0]  # R, G, B
            cubes = play.split(", ")

            for cube in cubes:
                count, colour = cube.split(" ")
                if colour == "red":
                    reveal[0] = int(count)
                elif colour == "green":
                    reveal[1] = int(count)
                elif colour == "blue":
                    reveal[2] = int(count)

            dataline.append(reveal)

        data.append(dataline)


# For each pass, identify its seat
def processData():
    possibles = 0
    # Possible with 12R, 13G, 14B
    for id, results in enumerate(data):
        valid = True
        for play in results:
            if play[0] > 12 or play[1] > 13 or play[2] > 14:
                valid = False
        if valid:
            possibles += id + 1

    return possibles


# Process harder
def processMore():
    power = 0
    # Possible with 12R, 13G, 14B
    for id, results in enumerate(data):
        minimums = [0, 0, 0]
        for play in results:
            if play[0] > minimums[0]:
                minimums[0] = play[0]
            if play[1] > minimums[1]:
                minimums[1] = play[1]
            if play[2] > minimums[2]:
                minimums[2] = play[2]

        power += prod(minimums)

    return power


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
