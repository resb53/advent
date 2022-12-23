#!/usr/bin/env python3

import argparse
import sys
from collections import deque, Counter

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = []
order = deque([-1j, 1j, -1, 1])


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    row = 0

    for line in input_fh:
        line = line.strip("\n")
        for x, v in enumerate(line):
            if v == "#":
                grid.append(x + row * 1j)
        row += 1


def printGrid():
    minx = min([int(x.real) for x in grid])
    maxx = max([int(x.real) for x in grid])
    miny = min([int(y.imag) for y in grid])
    maxy = max([int(y.imag) for y in grid])

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if x + y * 1j in grid:
                print("#", end="")
            else:
                print(".", end="")
        print("")


# One round of elf moving
def moveElves():
    plan = {}

    # Prepare a move
    for elf, pos in enumerate(grid):
        neighbours = getNeighbours(pos)
        if len(neighbours) == 0:
            plan[elf] = pos
        else:
            for dir in order:
                if dir not in neighbours:
                    plan[elf] = (pos + dir)
                    break
        if elf not in plan:
            plan[elf] = pos

    # Move as planned
    freq = Counter(plan.values())
    for elf in range(len(grid)):
        if freq[plan[elf]] == 1:
            grid[elf] = plan[elf]

    order.rotate(-1)


# List of blocked directions for a given elf
def getNeighbours(pos):
    blocked = set()
    n = [-1-1j, -1j, 1-1j]
    e = [1-1j, 1, 1+1j]
    s = [1+1j, 1j, -1+1j]
    w = [-1+1j, -1, -1-1j]

    for offset in n:
        if pos + offset in grid:
            blocked.add(-1j)
            break
    for offset in e:
        if pos + offset in grid:
            blocked.add(1)
            break
    for offset in s:
        if pos + offset in grid:
            blocked.add(1j)
            break
    for offset in w:
        if pos + offset in grid:
            blocked.add(-1)
            break

    return blocked


# Count gaps in smallest rectangle
def countGaps():
    minx = min([int(x.real) for x in grid])
    maxx = max([int(x.real) for x in grid])
    miny = min([int(y.imag) for y in grid])
    maxy = max([int(y.imag) for y in grid])

    total = (maxx - minx + 1) * (maxy - miny + 1)

    return total - len(grid)


# For each pass, identify its seat
def processData():
    for _ in range(10):
        moveElves()

    print(f"Part 1: {countGaps()}")


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
