#!/usr/bin/env python3

import argparse
import sys
import re
from collections import Counter, defaultdict
from math import prod
from copy import deepcopy

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

robots = []
maxv = (101, 103)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        m = re.match(r"^p\=(\d+),(\d+) v=(\-?\d+),(\-?\d+)$", line)
        if m[0] is None:
            sys.exit(f"Unable to parse: {line}")
        else:
            robots.append({
                "p": (int(m[1]), int(m[2])),
                "v": (int(m[3]), int(m[4]))
            })


# Predict movement of the robots
def processData():
    p1robots = deepcopy(robots)
    moveRobots(p1robots, 100)
    return quadrantise(p1robots)


# Move robots for n iterations
def moveRobots(rbts, n):
    grid = Counter()
    for robot in rbts:
        newpos = (
            (robot["p"][0] + (n * robot["v"][0])) % maxv[0],
            (robot["p"][1] + (n * robot["v"][1])) % maxv[1]
        )
        grid[newpos] += 1
        robot["p"] = newpos
    return grid


# Calculate score having split robots into quadrants
def quadrantise(rbts):
    mid = (maxv[0]//2, maxv[1]//2)
    quad = Counter()

    for robot in rbts:
        if robot["p"][0] < mid[0] and robot["p"][1] < mid[1]:
            quad["A"] += 1
        elif robot["p"][0] > mid[0] and robot["p"][1] < mid[1]:
            quad["B"] += 1
        elif robot["p"][0] > mid[0] and robot["p"][1] > mid[1]:
            quad["C"] += 1
        elif robot["p"][0] < mid[0] and robot["p"][1] > mid[1]:
            quad["D"] += 1

    return prod(quad.values())


# Find the Easter Egg
def processMore():
    t = 0
    p2robots = deepcopy(robots)
    # Find time when there are more than one line of 10 or more parallel robots
    while True:
        grid = moveRobots(p2robots, 1)
        t += 1
        poss = grid.keys()
        lines = Counter()

        rowstarts = defaultdict(list)
        for p in poss:
            row = followRight(grid, p, 10)
            if row:
                rowstarts[p[1]].append(p[0])
                lines[p[1]] += 1

        if len(lines.keys()) > 1:
            # Print JUST the Easter Egg
            miny = min(lines.keys())
            maxy = max(lines.keys())
            minx = min(rowstarts[miny])
            maxx = max(rowstarts[miny]) + 10
            printGrid(grid, minx, miny, maxx, maxy)
            # Return the Answer
            return t


# See if there's a row from a given point
def followRight(grid, p, length):
    neighbour = (p[0] + 1, p[1])
    if neighbour in grid:
        length -= 1
        if length > 0:
            return followRight(grid, neighbour, length)
        else:
            return True
    else:
        return False


# Print grid
def printGrid(grid, minx, miny, maxx, maxy):
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (x, y) in grid:
                print(str(grid[(x, y)]), end="")
            else:
                print(".", end="")
        print()


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
