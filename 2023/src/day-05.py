#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = defaultdict(list)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    key = ""
    for line in input_fh:
        line = line.rstrip()
        if len(line) > 0:
            parts = line.split(":")

            if len(parts) > 1:
                key = parts[0]
                if len(parts[1]) != 0:
                    # Get the seeds, not the leading space
                    data[key].extend(parts[1].split(" ")[1:])

            else:
                data[key].append(line.split(" "))

    print(data)


# Find lowest location number for any seed
def processData():
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
