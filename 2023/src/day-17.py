#!/usr/bin/env python3

import argparse
import sys
from heapq import heappop, heappush

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

weights = {}
moves = [1, 1j, -1, -1j]


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    for line in input_fh:
        line = line.rstrip()
        for x, val in enumerate(line):
            weights[complex(x, y)] = int(val)
        y += 1


# Shortest path without more than 3 movements inthe same direction
def shortestPaths(start, bounds):
    pq = [(0, start, 0, 0)]  # heat, pos, dir, straights
    distances = {}

    while len(pq) > 0:
        heat, pos, drn, straights = heappop(pq)
        for move in moves:
            newpos = pos + move
            if newpos.real < 0 or newpos.real > bounds[0] or newpos.imag < 0 or newpos.imag > bounds[1]:
                continue
            newstraights = straights
            if move == drn:
                newstraights += 1
            else:
                newstraights = 1
            if newstraights > 3:
                continue
            newheat = heat + weights[newpos]
            if newpos not in distances or (move, newstraights) not in distances[newpos]:
                distances[newpos] = {(move, newstraights): newheat}
                heappush(pq, (newheat, newpos, move, newstraights))
            elif newheat < distances[newpos][(move, newstraights)]:
                distances[newpos][(move, newstraights)] = newheat
                heappush(pq, (newheat, newpos, move, newstraights))

    print(distances)

    return False


# For each pass, identify its seat
def processData():
    start = 0
    bounds = (max([x.real for x in weights.keys()]), max([y.imag for y in weights.keys()]))
    return shortestPaths(start, bounds)


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
