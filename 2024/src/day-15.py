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
    for p in grid:
        if grid[p] == "O":
            total += 100 * int(p.imag) + int(p.real)

    return total


# Move the robot, and impacted boxes
def moveRobot(pos, dirn):
    newpos = pos + dirn
    if grid[newpos] == "#":
        return pos
    elif grid[newpos] == "O":
        if shiftBoxes(newpos, dirn):
            grid[pos] = "."
            grid[newpos] = "@"
            return newpos
        else:
            return pos
    elif grid[newpos] == ".":
        grid[pos] = "."
        grid[newpos] = "@"
        return newpos
    else:
        sys.exit(f"Unexpected object on grid: {grid[newpos]}")


# Iteratively move adjacent boxes
def shiftBoxes(pos, dirn):
    newpos = pos + dirn
    if grid[newpos] == "#":
        return False
    elif grid[newpos] == "O":
        if shiftBoxes(newpos, dirn):
            return True
        else:
            return False
    elif grid[newpos] == ".":
        grid[newpos] = "O"
        return True
    else:
        sys.exit(f"Unexpected object in boxshift: {grid[newpos]}")


# Process harder
def processMore(pos):
    maxv[0] *= 2
    for op in instr:
        pos = wideMoveRobot(pos, op)
    printGrid(biggrid)
    # Calculate GPS
    total = 0
    for p in biggrid:
        if biggrid[p] == "[":
            if int(p.imag) < (maxv[1] / 2):
                y = int(p.imag)
            else:
                y = maxv[1] - int(p.imag) - 1
            if int(p.real) < (maxv[0] / 2):
                x = int(p.real)
            else:
                x = maxv[0] - int(p.real) - 2
            total += 100 * y + x
    return total


# Move the robot, and impacted boxes
def wideMoveRobot(pos, dirn):
    newpos = pos + dirn
    if biggrid[newpos] == "#":
        return pos
    elif biggrid[newpos] == "[":
        box = [newpos, newpos+1]
        if wideShiftBoxes(box, dirn):
            biggrid[pos] = "."
            biggrid[newpos] = "@"
            return newpos
        else:
            return pos
    elif biggrid[newpos] == "]":
        box = [newpos-1, newpos]
        if wideShiftBoxes(box, dirn):
            biggrid[pos] = "."
            biggrid[newpos] = "@"
            return newpos
        else:
            return pos
    elif biggrid[newpos] == ".":
        biggrid[pos] = "."
        biggrid[newpos] = "@"
        return newpos


# Iteratively move adjacent boxes
def wideShiftBoxes(box, dirn):
    newbox = [p+dirn for p in box]

    # Horizontal
    if dirn.imag == 0:
        if dirn == -1:
            newpos = newbox[0]
        elif dirn == 1:
            newpos = newbox[1]

        if biggrid[newpos] == "#":
            return False
        elif (biggrid[newpos] == "[") or (biggrid[newpos] == "]"):
            nextbox = [p+dirn for p in newbox]
            if wideShiftBoxes(nextbox, dirn):
                biggrid[newbox[0]] = "["
                biggrid[newbox[1]] = "]"
                return True
            else:
                return False
        elif biggrid[newpos] == ".":
            biggrid[newbox[0]] = "["
            biggrid[newbox[1]] = "]"
            return True
    # Vertical
    elif dirn.real == 0:
        if (biggrid[newbox[0]] == "#") or (biggrid[newbox[1]] == "#"):
            return False
        elif (biggrid[newbox[0]] == "[") and (biggrid[newbox[1]] == "]"):
            if wideShiftBoxes(newbox, dirn):
                biggrid[newbox[0]] = "["
                biggrid[newbox[1]] = "]"
                biggrid[box[0]] = "."
                biggrid[box[1]] = "."
                return True
            else:
                return False
        elif (biggrid[newbox[0]] == "]") and (biggrid[newbox[1]] == "."):
            nextbox = [p-1 for p in newbox]
            if wideShiftBoxes(nextbox, dirn):
                biggrid[newbox[0]] = "["
                biggrid[newbox[1]] = "]"
                biggrid[box[0]] = "."
                biggrid[box[1]] = "."
                return True
            else:
                return False
        elif (biggrid[newbox[0]] == ".") and (biggrid[newbox[1]] == "["):
            nextbox = [p+1 for p in newbox]
            if wideShiftBoxes(nextbox, dirn):
                biggrid[newbox[0]] = "["
                biggrid[newbox[1]] = "]"
                biggrid[box[0]] = "."
                biggrid[box[1]] = "."
                return True
            else:
                return False
        elif (biggrid[newbox[0]] == "]") and (biggrid[newbox[1]] == "["):
            leftbox = [p-1 for p in newbox]
            rightbox = [p+1 for p in newbox]
            if wideShiftBoxes(leftbox, dirn) and wideShiftBoxes(rightbox, dirn):
                biggrid[newbox[0]] = "["
                biggrid[newbox[1]] = "]"
                biggrid[box[0]] = "."
                biggrid[box[1]] = "."
                return True
            else:
                return False
        elif (biggrid[newbox[0]] == ".") and (biggrid[newbox[1]] == "."):
            biggrid[newbox[0]] = "["
            biggrid[newbox[1]] = "]"
            biggrid[box[0]] = "."
            biggrid[box[1]] = "."
            return True


def main():
    pos1, pos2 = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(pos1)}")

    # Part 2
    print(f"Part 2: {processMore(pos2)}")


if __name__ == "__main__":
    main()
