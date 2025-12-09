#!/usr/bin/env python3

import argparse
import sys
from itertools import combinations
from shapely import Polygon

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


# Get rectangle polygon for pair of tiles
def getRect(a, b):
    return Polygon([a, (a[0], b[1]), b, (b[0], a[1])])


# For pair of red tiles find the largest rectangle area. For part 2 ensure they're entirely within the perimeter.
def processData():
    part1 = 0
    part2 = 0
    perimeter = Polygon(data)

    for pair in combinations(data, 2):
        area = getArea(pair[0], pair[1])
        rect = getRect(pair[0], pair[1])
        if area > part1:
            part1 = area
        if perimeter.contains(rect):
            if area > part2:
                part2 = area

    return part1, part2


def main():
    parseInput(args.input)
    part1, part2 = processData()

    # Part 1
    print(f"Part 1: {part1}")

    # Part 2
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
