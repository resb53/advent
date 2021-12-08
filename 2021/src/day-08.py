#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

segs = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}
univals = [2, 4, 3, 7]
nums = []
outs = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        first, last = line.strip("\n").split(" | ")
        nums.append(first.split(" "))
        outs.append(last.split(" "))


# For each pass, identify unique values
def processEasy():
    uniques = 0
    for output in outs:
        for digit in output:
            if len(digit) in univals:
                uniques += 1

    print(f"Solution to part 1: {uniques}")


# Process harder
def processHard():
    return False


def main():
    parseInput(args.input)

    # Part 1
    processEasy()

    # Part 2
    processHard()


if __name__ == "__main__":
    main()
