#!/usr/bin/env python3

import argparse
import sys
from itertools import combinations
from copy import deepcopy

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    for line in input_fh:
        line = line.rstrip()
        for x in [i for i, x in enumerate(line) if x == "#"]:
            data.append(x + y * 1j)
        y += 1


# Expand the universe
def expand(d):
    expanded = deepcopy(data)
    maxx = int(max([x.real for x in data]))
    maxy = int(max([y.imag for y in data]))

    # Find empty columns and rows
    empty = set()
    for x in range(maxx+1):
        void = True
        for pos in data:
            if pos.real == x:
                void = False
                break
        if void:
            empty.add(x)
    for y in range(maxy+1):
        void = True
        for pos in data:
            if pos.imag == y:
                void = False
                break
        if void:
            empty.add(y * 1j)

    # Expand empty rows by d
    for i, p in enumerate(expanded):
        countreal = 0
        countimag = 0

        for e in empty:
            if e.imag == 0:
                if p.real > e.real:
                    countreal += d
            if e.real == 0:
                if p.imag > e.imag:
                    countimag += d

        expanded[i] = p + countreal + countimag * 1j

    return expanded


# Calculate Manhattan distance between two points
def manhattan(a, b):
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


# Calculate shortest manhattan distance between each galaxys
def processData():
    expanded = expand(1)
    paths = 0
    for a, b in combinations(expanded, 2):
        paths += manhattan(a, b)
    return paths


# Calculate shortest distances with larger expansion
def processMore():
    expanded = expand(999999)
    paths = 0
    for a, b in combinations(expanded, 2):
        paths += manhattan(a, b)
    return paths


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
