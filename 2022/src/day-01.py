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

    newelf = True

    for line in input_fh:
        line = line.strip("\n")
        if len(line) == 0:
            newelf = True
        elif newelf:
            newelf = False
            data.append(int(line))
        else:
            data[-1] += int(line)


# For each pass, identify its seat
def processData():
    print(f"Part 1: {max(data)}")


# Process harder
def processMore():
    orderedData = sorted(data)
    print(f"Part 2: {orderedData[-3] + orderedData[-2] + orderedData[-1]}")


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
