#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Passport.")
parser.add_argument('input', metavar='input', type=str,
                    help='Password list input.')
args = parser.parse_args()

passes = []


def main():
    parseInput(args.input)

    # Part 1
    findSeats()

    # Part 2

    # Debug
    printSeats()


# Parse the input file
def parseInput(inp):
    global passes
    try:
        passes_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in passes_fh:
        passes.append(line.strip("\n"))


# For each pass, identify its seat
def findSeats():
    return True


def printSeats():
    for item in passes:
        print(item)


if __name__ == "__main__":
    main()
