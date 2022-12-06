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


# Find first element after 4 different elements
def processData():
    i = 4

    while True:
        uniques = len(set(data[i-4:i]))
        if uniques == 4:
            break
        else:
            i += 1

    print(f"Part 1: {i}")


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
