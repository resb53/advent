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

firstDigit = r'^.*?(\d)'
lastDigit = r'^.*(\d)'


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.append(line.strip("\n"))


# For each pass, identify its seat
def processData():
    total = 0

    for line in data:
        value = ''

        if (getFirst := re.match(firstDigit, line)) is not None:
            value += getFirst.group(1)
        else:
            sys.exit(f"Error: firstDigit not found in {line}.")

        if (getLast := re.match(lastDigit, line)) is not None:
            value += getLast.group(1)
        else:
            sys.exit(f"Error: firstDigit not found in {line}.")

        # print(value)
        total += int(value)

    print(f"Part 1: {total}")


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
