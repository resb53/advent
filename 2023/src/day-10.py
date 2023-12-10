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


# Go around the loop, return distance of full loop
def traverseLoop(start):
    pos = start
    dest = start + shapes[grid[start]][0]
    count = 0

    while dest != start:
        count += 1
        if dest + shapes[grid[dest]][0] != pos:
            pos = dest
            dest = dest + shapes[grid[dest]][0]
        else:
            pos = dest
            dest = dest + shapes[grid[dest]][1]

    return (count + 1) // 2


# Find the loop and it's most distant point
def processData(start):
    startShape(start)

    return traverseLoop(start)


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
