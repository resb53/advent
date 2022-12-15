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
            data.append([int(x) for x in (match[1], match[2], match[3], match[4])])
        else:
            print(f"Error parsing {line}")


# Calculate manhattan distance between two points
def getManhattan(coords):
    p1x, p1y, p2x, p2y = coords
    return abs(p1x - p2x) + abs(p1y - p2y)


# For each pass, identify its seat
def processData():
    row = set()
    rowno = 2000000

    for pair in data:
        mdist = getManhattan(pair)

        # if dection range intersects the target row
        if pair[1] <= rowno and pair[1] + mdist >= rowno:
            halfwidth = mdist - (rowno - pair[1])
            row.update(range(pair[0] - halfwidth, pair[0] + halfwidth + 1))
        elif pair[1] > rowno and pair[1] - mdist <= rowno:
            halfwidth = mdist - (pair[1] - rowno)
            row.update(range(pair[0] - halfwidth, pair[0] + halfwidth + 1))

    # Remove tiles with known beacons
    for pair in data:
        if pair[3] == rowno:
            row.discard(pair[2])

    print(f"Part 1: {len(row)}")


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
