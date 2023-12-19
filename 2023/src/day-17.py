#!/usr/bin/env python3

import argparse
import sys
from heapq import heappop, heappush
from numpy import complex64 as npcomplex

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()


# Implement wrapper for numpy complex numbers
def nplex(r, i):
    return npcomplex(complex(r, i))


weights = {}
moves = [nplex(1, 0), nplex(0, 1), nplex(-1, 0), nplex(0, -1)]


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
            weights[nplex(x, y)] = int(val)
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
            elif move == -drn:
                continue
            else:
                newstraights = 1
            if newstraights > 3:
                continue
            newheat = heat + weights[newpos]
            if newpos not in distances:
                distances[newpos] = {(move, newstraights): newheat}
                heappush(pq, (newheat, newpos, move, newstraights))
            elif (move, newstraights) not in distances[newpos] or newheat < distances[newpos][(move, newstraights)]:
                distances[newpos][(move, newstraights)] = newheat
                heappush(pq, (newheat, newpos, move, newstraights))

    # for x in range(0, bounds[0]+1):
    #     for y in range(0, bounds[1]+1):
    #         print(f"{nplex(x, y)}: {distances[nplex(x, y)]}")

    return min(distances[nplex(bounds[0], bounds[1])].values())


# For each pass, identify its seat
def processData():
    start = nplex(0, 0)
    bounds = (int(max([x.real for x in weights.keys()])), int(max([y.imag for y in weights.keys()])))
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
