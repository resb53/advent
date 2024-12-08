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
        data.append([int(x) for x in line.rstrip().split()])


# For each report, scan the levels to see if they're safe
def processData():
    safe = 0
    for report in data:
        scan = []
        for lvl in range(len(report) - 1):
            scan.append(report[lvl] - report[lvl + 1])
        # Check if always decreasing and no 0's
        if all(x < 0 for x in scan) or all(x > 0 for x in scan):
            # Check if all absolute values less than or equal to 3
            if all(abs(x) <= 3 for x in scan):
                safe += 1
    return safe


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
