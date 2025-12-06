#!/usr/bin/env python3

import argparse
import sys
from math import prod


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
        data.append(line.rstrip().split())


# Flip Data
def flipdata(d):
    flipped = []
    maxn = len(d) - 1

    for i in range(len(d[0])):
        calc = []

        for n in range(len(d)):
            if n < maxn:
                calc.append(int(d[n][i]))
            else:
                calc.insert(0, d[n][i])

        flipped.append(calc)

    return flipped


# Do cephlapod maths
def processData():
    grandtotal = 0
    flipped = flipdata(data)

    for calc in flipped:
        if calc[0] == "+":
            grandtotal += sum(calc[1:])
        else:
            grandtotal += prod(calc[1:])

    return grandtotal


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
