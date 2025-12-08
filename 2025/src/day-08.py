#!/usr/bin/env python3

import argparse
import sys
from math import sqrt, pow, prod
from itertools import combinations

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

    for line in input_fh:
        line = line.rstrip()
        data.append(tuple([int(x) for x in line.split(",")]))


# Find straight-line distance between two points
def straightDistance(a, b):
    return sqrt(pow((b[0] - a[0]), 2) + pow((b[1] - a[1]), 2) + pow((b[2] - a[2]), 2))


# Connect circuits
def connectCircuits(circuits, pair):
    a = -1
    b = -1

    for i, x in enumerate(circuits):
        if pair[0] in x:
            a = i
        if pair[1] in x:
            b = i

    if a == -1 or b == -1:
        sys.exit(f"Error: Cannot find {pair} in circuits.")

    if a == b:
        # Already connected
        return False
    else:
        circuits[a].extend(circuits[b])
        circuits.pop(b)


# Find shortest distance between points, connect the first 1000
def processData():
    distances = {}
    circuits = [[x] for x in data]

    for pair in combinations(data, 2):
        distances[(pair[0], pair[1])] = straightDistance(pair[0], pair[1])

    n = 0
    for pair in sorted(distances, key=distances.get):
        connectCircuits(circuits, pair)
        n += 1
        if n >= 1000:
            break

    circuits.sort(key=lambda x: len(x), reverse=True)

    return prod([len(x) for x in circuits[0:3]])


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
