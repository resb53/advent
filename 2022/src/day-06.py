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

    global data

    for line in input_fh:
        data = list(line.strip("\n"))


# Find first element after n different elements
def commonElements(n):
    i = n
    uniques = 0

    while uniques < n:
        uniques = len(set(data[i-n:i]))
        i += 1

    return i - 1 


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {commonElements(4)}")

    # Part 2
    print(f"Part 2: {commonElements(14)}")


if __name__ == "__main__":
    main()
