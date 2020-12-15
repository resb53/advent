#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Memory.")
parser.add_argument('input', metavar='input', type=str,
                    help='Numbers game input.')
args = parser.parse_args()

turns = []  # Reverse turn order so to use list.index()


def main():
    parseInput(args.input)

    # Part 1
    takeTurns(2020)
    print(turns[0])

    # Part 2

    # Debug
    #printTurns()


# Parse the input file
def parseInput(inp):
    global turns
    try:
        nums_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    line = nums_fh.readline()
    turns = list(reversed([int(i) for i in line.strip("\n").split(',')]))


# For each pass, identify its seat
def takeTurns(limit):
    global turns

    while len(turns) < limit:
        try:
            val = turns.index(turns[0], 1)
        except ValueError:
            val = 0
        turns.insert(0, val)


def printTurns():
    last = len(turns)  # Start at 1
    for turn, num in enumerate(turns):
        print(f", {last-turn}: {num}", end="")
    print("")


if __name__ == "__main__":
    main()
