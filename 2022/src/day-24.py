#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

bounds = [0, 0]  # maxx, maxy
blizzs = []
winds = {
    ">": 1,
    "v": 1j,
    "<": -1,
    "^": -1j
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    row = 0

    for line in input_fh:
        line = line.strip("\n")
        bounds[0] = len(line)
        for i, x in enumerate(line):
            if x in winds:
                blizzs.append([i + row * 1j, winds[x]])
        row += 1

    bounds[1] = row


# Print the grid
def printGrid():
    # Prepare the grid
    crosswinds = defaultdict(list)
    for blizz in blizzs:
        crosswinds[blizz[0]].append(blizz[1])

    # Print the grid
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            pos = x + y * 1j
            if pos == 1 or pos == (bounds[0] - 2) + (bounds[1] - 1) * 1j:
                print(".", end="")
            elif y == 0 or y == bounds[1] - 1 or x == 0 or x == bounds[0] - 1:
                print("#", end="")
            elif pos in crosswinds:
                if len(crosswinds[pos]) > 1:
                    print(len(crosswinds[pos]), end="")
                else:
                    print([k for k, v in winds.items() if v == crosswinds[pos][0]][0], end="")
            else:
                print(".", end="")
        print()


# Move the winds
def blowWinds():
    for blizz in blizzs:
        newpos = sum(blizz)
        if int(newpos.real) == 0:
            newpos += bounds[0] - 2
        elif int(newpos.imag) == 0:
            newpos += (bounds[1] - 2) * 1j
        elif int(newpos.real) == bounds[0] - 1:
            newpos -= bounds[0] - 2
        elif int(newpos.imag) == bounds[1] - 1:
            newpos -= (bounds[1] - 2) * 1j
        blizz[0] = newpos


# For each pass, identify its seat
def processData():
    printGrid()
    while True:
        _ = input()
        blowWinds()
        printGrid()


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
