#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    for line in input_fh:
        for x, chr in enumerate(line.rstrip()):
            grid[x + 1j * y] = chr
        y += 1


# Find occurrences of XMAS in the wordsearch
def processData():
    # For each X, check each direction and count occurrences
    count = 0
    for xpos in [pos for pos, val in grid.items() if val == "X"]:
        count += countxmas(xpos)
    return count


# Check each valid direction and increment counter if XMAS found
def countxmas(pos):
    count = 0
    for dir in [1, 1+1j, 1j, -1+1j, -1, -1-1j, -1j, 1-1j]:
        step = 1
        for match in ["M", "A", "S"]:
            check = pos + (dir * step)
            if check not in grid:
                break
            if match != grid[check]:
                break
            step += 1
        if step == 4:
            count += 1
    return count


# Find X-MAS instead of XMAS
def processMore():
    # For each A, check if it's the center of an X-MAS
    count = 0
    for apos in [pos for pos, val in grid.items() if val == "A"]:
        count += countx_mas(apos)
    return count


# Check each corner and increment if X-MAS found
def countx_mas(pos):
    m = 0
    s = 0
    for dir in [-1-1j, 1-1j, 1+1j, -1+1j]:
        loc = pos + dir
        if loc in grid:
            if grid[loc] == 'M':
                m += 1
            elif grid[loc] == 'S':
                s += 1
            else:
                break
        else:
            return 0
    if m != 2 or s != 2:
        return 0
    else:
        if grid[pos - 1-1j] != grid[pos + 1+1j]:
            return 1
        else:
            return 0


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
