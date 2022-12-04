#!/usr/bin/env python3

import argparse
import sys

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
        line = line.strip("\n")
        a, x = line.split(",")
        a, b = a.split("-")
        x, y = x.split("-")
        data.append([set(range(int(a), int(b) + 1)), set(range(int(x), int(y) + 1))])


# For each pass, identify its seat
def processData():
    contains = 0

    for pair in data:
        if pair[0].issubset(pair[1]) or pair[1].issubset(pair[0]):
            contains += 1

    print(f"Part 1: {contains}")


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
