#!/usr/bin/env python3

import argparse
import sys
import re

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
crates = [[] for _ in range(9)]


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    setup = []
    for _ in range(10):
        setup.append(input_fh.readline())

    for i in range(7, -1, -1):
        match = re.match(r"^(.{3}) (.{3}) (.{3}) (.{3}) (.{3}) (.{3}) (.{3}) (.{3}) (.{3})$", setup[i])

        if match is not None:
            for j in range(1, 10):
                if match[j] != "   ":
                    crates[j-1].append(match[j][1])

    print(crates)

    for line in input_fh:
        data.append(line.strip("\n"))


# Process crate instructions
def processData():
    return False


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
