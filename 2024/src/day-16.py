#!/usr/bin/env python3

import argparse
import sys
from copy import deepcopy

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
maxv = []
ops = {
    "^": 1,
    "<": 1000,
    ">": 1000
}
compass = [-1j, 1, 1j, -1]


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
            grid[x + 1j * y] = val
            if val == "S":
                s = x + 1j * y
        y += 1
    maxv.extend([x+1, y])

    return s


# Print the grid
def printGrid():
    for y in range(maxv[1]):
        for x in range(maxv[0]):
            print(grid[x + 1j * y], end="")
        print()


# Explore routes through the maze
def processData(start):
    routes = [["", [(start, 1)], 0]]  # Actions, Locations([pos, bearing]), Score
    completed = []
    c = 0
    while len(routes) > 0:
        newroutes = []
        for route in routes:
            for action in ops:
                if len(route[0]) > 0:
                    if action in "<>":
                        if route[0][-1] in "<>":
                            continue
                advance(deepcopy(route), action, newroutes, completed)
        routes = deepcopy(newroutes)
        c += 1
        print(f"Processing {c} turns, tracking {len(routes)} routes...", end="\r")
        # print(f"After {c} moves:")
        # for x in routes:
        #     print(x)
        # print("Completed:")
        # for x in completed:
        #     print(x)
        # print()

    return min([x[2] for x in completed])


# Advance reindeer a single move
def advance(route, action, routes, completed):
    route[0] += action
    pos = route[1][-1]
    match action:
        case "^":
            newpos = (pos[0]+pos[1], pos[1])
        case "<":
            newpos = (pos[0], compass[(compass.index(pos[1]) - 1) % 4])
        case ">":
            newpos = (pos[0], compass[(compass.index(pos[1]) + 1) % 4])
    # Check newpos is valid:
    # Don't go into a wall
    if grid[newpos[0]] == "#":
        return
    # Don't turn twice in a row (handled in calling function)
    # Don't revisit a location with the same bearing unless you've just turned on the spot
    elif newpos[0] in [x for x in route[1][0]] and action == "^":
        return
    else:
        route[1].append(newpos)
        route[2] += ops[action]
        if grid[newpos[0]] == "E":
            completed.append(route)
        else:
            routes.append(route)


# Process harder
def processMore():
    return False


def main():
    start = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(start)}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
