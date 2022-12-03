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


# Calculate priority score for element
def getScore(e):
    score = ord(e) - 96
    if score < 0:
        score += 58
    return score


# Find common element in each backpack
def findCommon(backpack):
    for ele in backpack[0]:
        if ele in backpack[1]:
            return getScore(ele)

    sys.exit("Shouldn't get here...")


# Find badge in each trio of backpacks
def findBadge(trio):
    for ele in trio[0]:
        if ele in trio[1] and ele in trio[2]:
            return getScore(ele)

    sys.exit("Shouldn't get here either...")


# For each pass, identify its seat
def processData():
    prioritysum = 0

    for backpack in data:
        prioritysum += findCommon(backpack)

    print(f"Part 1: {prioritysum}")


# Process harder
def processMore():
    badgesum = 0

    while len(data) > 0:
        trio = []
        for _ in range(3):
            backpack = data.pop(0)
            trio.append(backpack[0] + backpack[1])

        badgesum += findBadge(trio)

    print(f"Part 2: {badgesum}")


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
