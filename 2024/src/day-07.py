#!/usr/bin/env python3

import argparse
import sys
from itertools import product

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
        target, parts = line.rstrip().split(": ")
        values = [int(x) for x in parts.split(" ")]
        data.append([int(target), values])


# For each target, identify if it can be made with the given values, + and *
def processData():
    total = 0
    for target, values in data:
        for ops in product("SM", repeat=len(values) - 1):
            if calculate(values, ops) == target:
                total += target
                break
    return total


# Calculate equation
def calculate(vals, ops):
    lhs = vals[0]
    for i in range(1, len(vals)):
        if ops[i-1] == "S":
            lhs += vals[i]
        else:
            lhs *= vals[i]
    return lhs


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
