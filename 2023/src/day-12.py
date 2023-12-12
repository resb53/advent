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

'''
Plan:
- Create recursive function that ultimately returns 1 if a valid combination is found, or 0 if not, and sums these.
- Start from the left, find the first valid match of the first valid group.
- Kick off one recursion using that, and proceeding
    - Returning 0 if it doesn't complete.
    - Return 1 if it gets to the end of a valid line.
- Move past the first ? and start a new recursion pattern.
- Move past a # and move to next group if valid count (Need to think this through more)
'''


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        (line, arr) = line.rstrip().split()
        arr = [int(x) for x in arr.split(",")]
        data.append([line, arr])


# Calculate number of arrangements for a given pattern
def arrange(line, arr):
    print(line, arr)
    # Locate first possible location from left
    poss = re.match(r"^\.*[?#]{" + str(arr[0]) + "}(?!#)", line)
    # Distance to next considered point
    seen = re.match(r"^\.*(?:#+|\?)", line)

    if poss is not None:
        print(f"Poss: {poss[0]}")
    if seen is not None:
        print(f"Seen: {seen[0]}")

    return 1


# For each line of spring, work out how many possible arrangements
def processData():
    arrangements = 0
    for element in data:
        arrangements += arrange(element[0], element[1])
    return arrangements


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
