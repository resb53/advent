#!/usr/bin/env python3

import argparse
import sys
from itertools import combinations

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
        line = line.rstrip()
        data.append(tuple([int(x) for x in line.split(",")]))


# Get area for a pair of tiles
def getArea(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


# For pair of red tiles find the largest rectangle area
def processData():
    largest = 0
    for pair in combinations(data, 2):
        area = getArea(pair[0], pair[1])
        if area > largest:
            largest = area

    return largest


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
