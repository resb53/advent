#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

plots = set()
dirs = [1, 1j, -1, -1j]
bounds = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    maxx = 0
    start = 0
    for line in input_fh:
        line = line.rstrip()
        if maxx == 0:
            maxx = len(line)
        for x, val in enumerate(line):
            if val == ".":
                plots.add(complex(x, y))
            elif val == "S":
                start = complex(x, y)
                plots.add(complex(x, y))
        y += 1
    bounds.extend([maxx, y])
    return start


def incrementPositions(pos: set) -> set:
    newpos = set()
    for p in pos:
        for newp in [p + x for x in dirs]:
            if newp in plots:
                newpos.add(newp)
    return newpos


# Plots reachable by 64 steps
def processData(start, moves):
    pos = set([start])
    for _ in range(moves):
        pos = incrementPositions(pos)
    return len(pos)


# Process harder
def processMore(start, moves):
    pos = set([start])
    for _ in range(moves):
        pos = incrementPositions(pos)
    return len(pos)


def main():
    start = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(start, 64)}")

    # Part 2
    print(f"Part 2: {processMore(start, 26501365)}")


if __name__ == "__main__":
    main()
