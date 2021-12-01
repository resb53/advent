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
        data.append(line.strip("\n"))


# For each pass, identify its seat
def increasingDepth():
    deeper = 0
    current = data[0]
    for element in data:
        if element > current:
            deeper += 1
        current = element
    print(f"Depth increases: {deeper}")


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    increasingDepth()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
