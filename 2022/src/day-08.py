#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

# data[y][x], top-left (0,0)
data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.append([int(x) for x in line.strip("\n")])


# For each column / row / direction, count the visible trees
def processData():
    visible = defaultdict(int)

    maxy = len(data)
    maxx = len(data[0])

    # x: 0 -> n
    for row in range(maxy):
        tallest = -1
        for col in range(maxx):
            height = data[row][col]
            if height > tallest:
                visible[row + col * 1j] += 1
                tallest = height

    # y: n -> 0
    for col in range(maxx):
        tallest = -1
        for row in range(maxy-1, -1, -1):
            height = data[row][col]
            if height > tallest:
                visible[row + col * 1j] += 1
                tallest = height

    # x: n -> 0
    for row in range(maxy-1, -1, -1):
        tallest = -1
        for col in range(maxx-1, -1, -1):
            height = data[row][col]
            if height > tallest:
                visible[row + col * 1j] += 1
                tallest = height

    # y: 0 -> n
    for col in range(maxx-1, -1, -1):
        tallest = -1
        for row in range(maxy):
            height = data[row][col]
            if height > tallest:
                visible[row + col * 1j] += 1
                tallest = height

    print(f"Part 1: {len(visible)}")


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
