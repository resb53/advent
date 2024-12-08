#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

lhs = []
rhs = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        values = line.rstrip()
        left, right = values.split()
        lhs.append(int(left))
        rhs.append(int(right))


# For each pass, identify its seat
def processData():
    # Sort Arrays
    lhs.sort()
    rhs.sort()
    # Iterate through and calculate
    total = 0
    for i in range(len(lhs)):
        total += abs(lhs[i] - rhs[i])
    return total


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
