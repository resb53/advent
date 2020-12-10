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
device = 0


def main():
    global device

    parseInput(args.input)
    device = max(adapters) + 3

    # Part 1
    diff = (findDiffs())
    print(f"{diff}\nPart 1: {diff[1]*diff[3]}")

    # Part 2

    # Debug
    printAdapters()


# Parse the input file
def parseInput(inp):
    global adapters
    try:
        adapters_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in adapters_fh:
        adapters.append(int(line.strip("\n")))


# For each pass, identify its seat
def findDiffs():
    adaptsort = adapters.copy()
    adaptsort.extend([outlet, device])
    adaptsort.sort()
    diffs = {1: 0, 2: 0, 3: 0}

    for first, second in zip(adaptsort, adaptsort[1:]):
        diffs[second-first] += 1

    return diffs


def printAdapters():
    for item in adapters:
        print(item)


if __name__ == "__main__":
    main()
