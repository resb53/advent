#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

ranges = []
data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        if "-" in line:
            insert = -1
            r = [int(x) for x in line.split("-")]
            for i, x in enumerate(ranges):
                if r[0] > x[0]:
                    continue
                elif r[0] == x[0]:
                    if r[1] > x[1]:
                        continue
                    else:
                        insert = i
                        break
                else:
                    insert = i
                    break
            if insert == -1:
                ranges.append(r)
            else:
                ranges.insert(insert, r)
        elif len(line) > 0:
            data.append(int(line))


# Collapse fresh ranges
def collapseRanges():
    return 0


# Find fresh ingredients
def processData():
    for r in ranges:
        print(f"{r[0]} -> {r[1]}")
    for element in data:
        print(f"{element}")
    return False


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
