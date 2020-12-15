#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Memory.")
parser.add_argument('input', metavar='input', type=str,
                    help='Numbers game input.')
args = parser.parse_args()

turns = []


def main():
    parseInput(args.input)

    # Part 1
    takeTurns(2020)

    # Part 2

    # Debug
    printTurns()


# Parse the input file
def parseInput(inp):
    global turns
    try:
        nums_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    line = nums_fh.readline()
    turns = [int(i) for i in line.strip("\n").split(',')]


# For each pass, identify its seat
def takeTurns(limit):
    return True


def printTurns():
    print(f"0: {turns[0]}", end="")
    for turn, num in enumerate(turns, 1):
        print(f", {turn}: {num}", end="")
    print("")


if __name__ == "__main__":
    main()
