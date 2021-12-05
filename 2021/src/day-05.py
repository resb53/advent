#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
grid = defaultdict(int)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.append(line.strip("\n"))


# Only consider horizontal lines
def processHorizontals():
    for line in data:
        temp = []
        points = line.split(" -> ")
        for point in points:
            (re, im) = point.split(",")
            temp.append(int(re) + int(im) * 1j)
        if (temp[0].real == temp[1].real):
            start = int(min(temp[0].imag, temp[1].imag))
            stop = int(max(temp[0].imag, temp[1].imag))
            for v in range(start, stop + 1):
                grid[temp[0].real + v * 1j] += 1
        elif (temp[0].imag == temp[1].imag):
            start = int(min(temp[0].real, temp[1].real))
            stop = int(max(temp[0].real, temp[1].real))
            for v in range(start, stop + 1):
                grid[v + temp[0].imag * 1j] += 1
        # Process Diagonals
        else:
            # TLBR
            if (temp[0].real < temp[1].real) and (temp[0].imag < temp[1].imag):
                for step in range(int(temp[1].real - temp[0].real) + 1):
                    grid[temp[0].real + step + (temp[0].imag + step) * 1j] += 1
            elif (temp[0].real > temp[1].real) and (temp[0].imag > temp[1].imag):
                for step in range(int(temp[0].real - temp[1].real) + 1):
                    grid[temp[1].real + step + (temp[1].imag + step) * 1j] += 1
            # TRBL
            elif (temp[0].real < temp[1].real) and (temp[0].imag > temp[1].imag):
                for step in range(int(temp[1].real - temp[0].real) + 1):
                    grid[temp[0].real + step + (temp[0].imag - step) * 1j] += 1
            elif (temp[0].real > temp[1].real) and (temp[0].imag < temp[1].imag):
                for step in range(int(temp[0].real - temp[1].real) + 1):
                    grid[temp[1].real + step + (temp[1].imag - step) * 1j] += 1

    # Debug visualisation for test input
    """for y in range(10):
        for x in range(10):
            if (grid[x + y * 1j] == 0):
                print(".", end="")
            else:
                print(grid[x + y * 1j], end="")
        print("\n", end="")"""

    count = 0
    for loc in grid:
        if (grid[loc] > 1):
            count += 1

    print(f"Solution: {count}")


# Process diagonals
def processDiagonals():
    return False


def main():
    parseInput(args.input)

    # Part 1
    processHorizontals()

    # Part 2
    processDiagonals()


if __name__ == "__main__":
    main()
