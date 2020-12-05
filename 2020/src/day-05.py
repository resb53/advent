#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Passport.")
parser.add_argument('input', metavar='input', type=str,
                    help='Password list input.')
args = parser.parse_args()

passes = []
rows = 128
cols = 8


def main():
    parseInput(args.input)

    # Part 1
    findSeats()

    # Part 2

    # Debug
    # printSeats()


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
    maxseat = 0

    for item in passes:
        minrow = 0
        maxrow = rows - 1
        mincol = 0
        maxcol = cols - 1

        for char in item:
            if char == 'F':
                maxrow = int((maxrow - minrow)/2) + minrow
            elif char == 'B':
                minrow = int((maxrow - minrow)/2) + 1 + minrow
            if char == 'L':
                maxcol = int((maxcol - mincol)/2) + mincol
            elif char == 'R':
                mincol = int((maxcol - mincol)/2) + 1 + mincol

        if minrow != maxrow or mincol != maxcol:
            sys.exit(f"Error for pass {item}: Item: {item}, Minrow: {minrow},",
                     f"Maxrow: {maxrow}, Mincol: {mincol}, Maxcol: {maxcol}")

        # Calculate seat
        seat = minrow * 8 + mincol
        if seat > maxseat:
            maxseat = seat
    
    print(maxseat)


def printSeats():
    for item in passes:
        print(item)


if __name__ == "__main__":
    main()
