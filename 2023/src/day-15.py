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
        data.extend(line.rstrip().split(","))


# Sum the hashes of the lines
def processData():
    hashsum = 0
    for x in data:
        linehash = 0
        for c in x:
            linehash += ord(c)
            linehash *= 17
            linehash %= 256
        hashsum += linehash
    return hashsum


# Insert the lenses using HASHMAP
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
