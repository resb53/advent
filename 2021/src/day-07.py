#!/usr/bin/env python3

import argparse
import sys
from math import ceil
import numpy

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

crabs = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for val in input_fh.readline().strip("\n").split(','):
        crabs.append(int(val))


# Calculate min fuel cost
def processData():
    sd = ceil(numpy.std(crabs))
    mean = int(numpy.mean(crabs))
    minv = min(crabs)
    maxv = max(crabs)
    start = minv
    stop = maxv

    # Calculate within a standard deviation of the mean to begin
    if mean - sd > start:
        start = mean - sd
    if mean + sd < stop:
        stop = mean + sd

    fuelcost = {}

    # for test in range(start, stop+1, 1):
    for test in range(minv, maxv+1, 1):
        fuel = 0
        for c in crabs:
            fuel += abs(c - test)
        fuelcost[test] = fuel

    print(f"Solution to part 1: {min(fuelcost.values())}")


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
