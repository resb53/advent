#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
folds = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    folding = False
    for line in input_fh:
        line = line.strip("\n")
        if len(line) == 0:
            folding = True
        elif not folding:
            (x, y) = line.split(',')
            grid[int(x) + int(y) * 1j] = 1
        else:
            folds.append((line[11], int(line[13:])))


# For each pass, identify its seat
def processFolds():
    for fold in folds:
        if fold[0] == "y":
            foldHorizontally(fold[1])
        else:
            foldVertically(fold[1])
        print(len(grid))


def foldHorizontally(fold):
    dots = list(grid.keys())
    for dot in dots:
        if dot.imag > fold:
            grid.pop(dot)
            grid[dot.real + (2 * fold - dot.imag) * 1j] = 1


def foldVertically(fold):
    dots = list(grid.keys())
    for dot in dots:
        if dot.real > fold:
            grid.pop(dot)
            grid[(2 * fold - dot.real) + dot.imag * 1j] = 1


def main():
    parseInput(args.input)

    # Part 1 (and 2?)
    processFolds()


if __name__ == "__main__":
    main()
