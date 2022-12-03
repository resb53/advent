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
        line = line.strip("\n")
        mid = len(line) // 2
        data.append([line[0:mid], line[mid:]])


# Find common element in each backpack
def findCommon(backpack):
    for ele in backpack[0]:
        if ele in backpack[1]:
            score = ord(ele) - 96
            if score < 0:
                score += 58
            return score

    sys.exit("Shouldn't get here...")


# For each pass, identify its seat
def processData():
    prioritysum = 0

    for backpack in data:
        priority = findCommon(backpack)
        prioritysum += priority

    print(f"Part 1: {prioritysum}")


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
