#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
bounds = []
shapes = {
    "|": [-1j, 1j],
    "-": [-1, 1],
    "L": [-1j, 1],
    "J": [-1, -1j],
    "7": [-1, 1j],
    "F": [1j, 1],
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = -1
    start = 0
    for line in input_fh:
        line = line.rstrip()
        y += 1
        if len(bounds) == 0:
            bounds.append(len(line) - 1)
        for x, tile in enumerate(line):
            grid[x + y * 1j] = tile
            if tile == "S":
                start = x + y * 1j

    bounds.append(y)

    return start


# Get shape of start
def startShape(start):
    connections = ""
    if (start - 1j) in grid:
        if grid[start - 1j] in "|7F":
            connections += "N"
    if (start + 1) in grid:
        if grid[start + 1] in "-J7":
            connections += "E"
    if (start + 1j) in grid:
        if grid[start + 1j] in "|LJ":
            connections += "S"
    if (start - 1) in grid:
        if grid[start - 1] in "-LF":
            connections += "W"

    if len(connections) != 2:
        raise ValueError("Start must be connected to two pipes.")
    else:
        match connections:
            case "NS":
                grid[start] = "|"
            case "EW":
                grid[start] = "-"
            case "NE":
                grid[start] = "L"
            case "NW":
                grid[start] = "J"
            case "SW":
                grid[start] = "7"
            case "ES":
                grid[start] = "F"

    return None


# Go around the loop, return loop path
def traverseLoop(start):
    loop = [start]
    dest = start + shapes[grid[start]][0]

    while dest != loop[0]:
        if dest + shapes[grid[dest]][0] != loop[-1]:
            loop.append(dest)
            dest = dest + shapes[grid[dest]][0]
        else:
            loop.append(dest)
            dest = dest + shapes[grid[dest]][1]

    return loop


# Find the loop and it's most distant point
def processData(start):
    startShape(start)

    return traverseLoop(start)


# Extend the grid
def extendGrid():
    bounds[0] += 1
    bounds[1] += 1

    for y in range(-1, bounds[1]+1):
        grid[-1 + y * 1j] = "."
        grid[bounds[0] + y * 1j] = "."

    for x in range(-1, bounds[0]+1):
        grid[x - 1j] = "."
        grid[x + bounds[1] * 1j] = "."


# Get neighbours of a grid location
def getNeighbours(pos):
    neighbours = []
    for x in [-1j, 1-1j, 1, 1+1j, 1j, -1+1j, -1, -1-1j]:
        if (pos + x).imag >= -1 and \
           (pos + x).real <= bounds[0] and \
           (pos + x).imag <= bounds[1] and \
           (pos + x).real >= -1:
            neighbours.append(pos + x)

    return neighbours


# Go through grid filling connected space
def fillSpace(pos, filled, loop):
    # Get pos neighbours in extended bounds
    newfills = []
    for tile in getNeighbours(pos):
        if tile not in filled and tile not in loop:
            filled.append(tile)
            newfills.append(tile)
    for tile in newfills:
        fillSpace(tile, filled, loop)


# Find the points enclosed by the loop
# = Grid area - points not enclosed - points on the loop
# extend bounds by 1 to ensure no trapped external areas
def processMore(loop):
    extendGrid()
    totalarea = (bounds[0] + 1) * (bounds[1] + 1)
    beginfill = -1-1j
    filled = [beginfill]

    fillSpace(beginfill, filled, loop)

    # Print extended grid
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            p = x + y * 1j
            if p in filled:
                print("X", end="")
            else:
                print(grid[p], end="")
        print()

    # Remove extended edges
    filledcount = len(filled) - (bounds[0] + 2) - (bounds[1] + 2)

    return totalarea - filledcount - len(loop)


def main():
    start = parseInput(args.input)
    loop = processData(start)

    # Part 1
    print(f"Part 1: {len(loop) // 2}")

    # Part 2
    print(f"Part 2: {processMore(loop)}")


if __name__ == "__main__":
    main()
