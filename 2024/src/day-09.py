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
        digits = [int(x) for x in line.rstrip()]
        free = False
        id = 0
        for x in digits:
            if not free:
                data.extend([id] * x)
                free = not free
                id += 1
            else:
                data.extend(["."] * x)
                free = not free


# Move blocks to leftmost free space, and calculate resulting checksum
def processData():
    lastblock, firstspace = updateStatus()
    while lastblock > firstspace:
        data[firstspace] = data[lastblock]
        data[lastblock] = "."
        lastblock, firstspace = updateStatus()
    return checksum(data)


# Update current status
def updateStatus():
    for i in range(len(data)-1, -1, -1):
        if data[i] != ".":
            lastblock = i
            break
    firstspace = data.index(".")

    return lastblock, firstspace


# Get checksum of filesystem
def checksum(fs):
    total = 0
    for i, x in enumerate(fs):
        if x != ".":
            total += i * x
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
