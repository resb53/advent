#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

lookup = {}
grid = {}


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


# For each pass, identify its seat
def processData():
    print(lookup)
    print(grid)


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
