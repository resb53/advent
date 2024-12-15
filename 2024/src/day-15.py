#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
biggrid  = {}
maxv = []
instr = []
dirn = {
    ">": 1,
    "v": 1j,
    "<": -1,
    "^": -1j
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    instread = False
    y = 0
    pos = -1-1j

    for line in input_fh:
        line = line.rstrip()

        if len(line) == 0:
            instread = True
        else:
            if not instread:
                for x, val in enumerate(line):
                    grid[x + 1j * y] = val
                    if val == "@":
                        pos1 = x + 1j * y
            else:
                for x in line:
                    instr.append(dirn[x])
        if not instread:
            y += 1

    maxv.extend([max([int(x.real) for x in grid.keys()])+1, y])

    # For part 2
    pos2 = embiggenGrid()

    return pos1, pos2


# Print the grid
def printGrid(g):
    for y in range(maxv[1]):
        for x in range(maxv[0]):
            print(g[x + 1j * y], end="")
        print()


# Iterate through the robots moves, updating the grid as we go, and calculate the total GPS
def processData(pos):
    for op in instr:
        pos = moveRobot(pos, op)
    # Calculate GPS
    total = 0
    for pos in grid:
        if grid[pos] == "O":
            total += 100 * int(pos.imag) + int(pos.real)

    return total


# Move the robot, and impacted boxes
def moveRobot(pos, dirn):
    newpos = pos + dirn
    if grid[newpos] == "#":
        return pos
    elif grid[newpos] == ".":
        grid[pos] = "."
        grid[newpos] = "@"
        return newpos
    elif grid[newpos] == "O":
        if shiftBoxes(newpos, dirn):
            grid[pos] = "."
            grid[newpos] = "@"
            return newpos
        else:
            return pos
    else:
        sys.exit(f"Unexpected object on grid: {grid[newpos]}")


# Iteratively move adjacent boxes
def shiftBoxes(pos, dirn):
    newpos = pos + dirn
    if grid[newpos] == "#":
        return False
    elif grid[newpos] == "O":
        if not shiftBoxes(newpos, dirn):
            return False
        else:
            return True
    elif grid[newpos] == ".":
        grid[newpos] = "O"
        return True
    else:
        sys.exit(f"Unexpected object in boxshift: {grid[newpos]}")


# Process harder
def processMore(pos):
    maxv[0] *= 2
    printGrid(biggrid)
    print(f"Pos: {pos}")
    return False


# Enlarge the grid for part 2
def embiggenGrid():
    pos = -1-1j
    for y in range(maxv[1]):
        for x in range(maxv[0]):
            if grid[x + 1j * y] == "#":
                biggrid[2 * x + 1j * y] = "#"
                biggrid[2 * x + 1 + 1j * y] = "#"
            elif grid[x + 1j * y] == "O":
                biggrid[2 * x + 1j * y] = "["
                biggrid[2 * x + 1 + 1j * y] = "]"
            elif grid[x + 1j * y] == ".":
                biggrid[2 * x + 1j * y] = "."
                biggrid[2 * x + 1 + 1j * y] = "."
            elif grid[x + 1j * y] == "@":
                biggrid[2 * x + 1j * y] = "@"
                pos = 2 * x + 1j * y
                biggrid[2 * x + 1 + 1j * y] = "."

    return pos


def main():
    pos1, pos2 = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(pos1)}")

    # Part 2
    print(f"Part 2: {processMore(pos2)}")


if __name__ == "__main__":
    main()
