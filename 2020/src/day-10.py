#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Adapters.")
parser.add_argument('input', metavar='input', type=str,
                    help='Adapter list input.')
args = parser.parse_args()

adapters = []
outlet = 0


def main():
    parseInput(args.input)

    # Part 1
    diff = (findDiffs())
    print(f"{diff}\nPart 1: {diff[1]*diff[3]}")

    # Part 2
    arrangements()

    # Debug
    # printAdapters()


# Parse the input file
def parseInput(inp):
    global adapters
    try:
        adapters_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in adapters_fh:
        adapters.append(int(line.strip("\n")))

    adapters.extend([outlet, max(adapters)+3])
    adapters.sort()


# For each pass, identify its seat
def findDiffs():
    diffs = {1: 0, 2: 0, 3: 0}

    for first, second in zip(adapters, adapters[1:]):
        diffs[second-first] += 1

    return diffs


# Find all possible arrangements
def arrangements():
    # Iterate across sorted list
    return True

def printAdapters():
    for item in adapters:
        print(item)


if __name__ == "__main__":
    main()
