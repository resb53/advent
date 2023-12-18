#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
grid = []
compass = {
    "U": -1j,
    "R": 1,
    "D": 1j,
    "L": -1
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        vals = line.rstrip().split()
        data.append([vals[0], int(vals[1]), vals[2].strip("(#)")])


# Dig edges of plan
def dig(plan):
    start = 0
    for instr in plan:
        drn = instr[0]
        length = instr[1]
        dest = start + length * compass[drn]
        grid.append((start, dest))
        start = dest


# Showlace area (Gauss) https://www.theoremoftheday.org/GeometryAndTrigonometry/Shoelace/TotDShoelace.pdf
def shoelace():
    dblarea = 0
    for edge in grid:
        dblarea += edge[0].real * edge[1].imag - edge[1].real * edge[0].imag
    area = dblarea / 2

    # Add the edges (inclusive)
    edges = 0
    for edge in grid:
        edges += abs(edge[1] - edge[0])
    area += edges/2 + 1

    return area


# Get digger to dig following a set of instructions
def processData():
    dig(data)
    return int(shoelace())


# Dig with the colour codes!
def processMore():
    grid.clear()
    cdig = []
    drn = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U"
    }
    for vals in data:
        hexlen = int(vals[2][0:5], 16)
        hexdrn = vals[2][5]
        cdig.append([drn[hexdrn], hexlen])

    dig(cdig)
    return int(shoelace())


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
