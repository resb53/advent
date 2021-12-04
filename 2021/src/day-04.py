#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

rows = defaultdict(list)
cols = defaultdict(list)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    # Get call list
    call = input_fh.readline().strip("\n").split(',')

    # Generate rows per board
    count = -1

    for line in input_fh:
        line = line.strip("\n")
        if len(line) == 0:
            count += 1
        else:
            rows[count].append([])
            row = line.split()
            for n in row:
                rows[count][-1].append([int(n), 0])

    # Generate columns per board
    for board in rows:
        for i in range(5):
            cols[board].append([])
            for r in rows[board]:
                cols[board][-1].append([r[i][0], 0])

    return call


# For each pass, identify its seat
def processData(call):
    for element in call:
        print(f"{element}", end=", ")


# Process harder
def processMore():
    return False


def main():
    call = parseInput(args.input)

    # Part 1
    processData(call)

    # Part 2
    # processMore()


if __name__ == "__main__":
    main()
