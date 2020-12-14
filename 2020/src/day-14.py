#!/usr/bin/python3

import argparse
import sys
import re

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Bitmask.")
parser.add_argument('input', metavar='input', type=str,
                    help='Bitwise data input.')
args = parser.parse_args()

data = []


def main():
    parseInput(args.input)

    # Part 1
    findInit()

    # Part 2

    # Debug
    printData()


# Parse the input file
def parseInput(inp):
    global data
    mask = ''
    try:
        data_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in data_fh:
        match = re.match(r"^mem\[(\d+)\] = (\d+)$", line, re.I)
        if not match:
            mask = line.split(" = ")[1]
            print(f"New mask: {mask}")
        else:
            data.append((int(match.group(1)), int(match.group(2))))


# For each pass, identify its seat
def findInit():
    return True


def printData():
    for item in data:
        print(item)


if __name__ == "__main__":
    main()
