#!/usr/bin/env python3

import argparse
import sys
import re

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
        match = re.match(r"^Sensor at x=(\-?\d+), y=(\-?\d+): closest beacon is at x=(\-?\d+), y=(\-?\d+)", line)
        if match is not None:
            coords = [int(x) for x in (match[1], match[2], match[3], match[4])]
            coords.append(getManhattan(coords))
            data.append([int(x) for x in coords])
        else:
            print(f"Error parsing {line}")


# Calculate manhattan distance between two points
def getManhattan(coords):
    p1x, p1y, p2x, p2y = coords
    return abs(p1x - p2x) + abs(p1y - p2y)


# For given row, calculate how many positions a beacon can't be in
def processData():
    row = set()
    rowno = 2000000

    for pair in data:
        mdist = pair[4]

        # if dection range intersects the target row
        halfwidth = mdist - abs(rowno - pair[1])
        if halfwidth >= 0:
            row.update(range(pair[0] - halfwidth, pair[0] + halfwidth + 1))

    # Remove tiles with known beacons
    for pair in data:
        if pair[3] == rowno:
            row.discard(pair[2])

    print(f"Part 1: {len(row)}")


# Find the only possible location of the hidden beacon
def processMore():
    minvalue = 0
    maxvalue = 4000000

    for rowno in range(minvalue, maxvalue + 1):
        print(rowno, end="\r")
        edges = set()

        for pair in data:
            mdist = pair[4]

            # if dection range intersects the target row
            halfwidth = mdist - abs(rowno - pair[1])
            if halfwidth >= 0:
                edges.add((max(minvalue, pair[0] - halfwidth), min(maxvalue, pair[0] + halfwidth)))

        # See if there's a gap:
        last = 0
        for ends in sorted(edges):
            if ends[0] > last + 1:
                return (last + 1, rowno)
            elif ends[1] > last:
                last = ends[1]


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    location = processMore()
    if location is not None:
        print(f"Part 2: {4000000 * location[0] + location[1]}")


if __name__ == "__main__":
    main()
