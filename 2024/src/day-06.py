#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
maxv = [0, 0]
dirn = {
    "^": -1j,
    ">": 1,
    "v": 1j,
    "<": -1
}
di = [-1j, 1, 1j, -1]
visited = set()


# Parse the input file
def parseInput(inp):
    guard = [0, 1]  # pos, dirn
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    x = 0

    for line in input_fh:
        line = line.rstrip()
        for x, val in enumerate(line):
            if val in dirn:
                guard[0] = x + y * 1j
                guard[1] = dirn[val]
                visited.add(x + y * 1j)
                grid[x + y * 1j] = '.'
            else:
                grid[x + y * 1j] = val
        y += 1

    maxv[0] = x + 1
    maxv[1] = y

    return guard


# Inspect Room
def printGrid():
    for y in range(maxv[1]):
        for x in range(maxv[0]):
            print(grid[x + y * 1j], end="")
        print()


# Trace the guards route
def processData(guard):
    while (int(guard[0].real) >= 0 and int(guard[0].real) <= maxv[0]
           and int(guard[0].imag) >= 0 and int(guard[0].imag) <= maxv[1]):
        newpos = guard[0] + guard[1]
        if newpos in grid:
            if grid[newpos] == '.':
                guard[0] = newpos
                visited.add(newpos)
            else:
                guard[1] = di[(di.index(guard[1]) + 1) % 4]
        else:
            return len(visited)
    return False


# Find all potential obstacle positions that create loops
def processMore(origin):
    # Obstacles can only be on visited squares to have an impact, but can't be on the origial square
    visited.remove(origin[0])
    loops = 0

    for x in visited:
        newgrid = grid.copy()
        newgrid[x] = "#"
        guard = origin.copy()
        tracked = set([tuple(guard)])

        while (int(guard[0].real) >= 0 and int(guard[0].real) <= maxv[0]
               and int(guard[0].imag) >= 0 and int(guard[0].imag) <= maxv[1]):
            newpos = guard[0] + guard[1]
            if newpos in newgrid:
                if newgrid[newpos] == '.':
                    guard[0] = newpos
                    if tuple(guard) in tracked:
                        loops += 1
                        break
                    else:
                        tracked.add(tuple(guard))
                else:
                    guard[1] = di[(di.index(guard[1]) + 1) % 4]
                    if tuple(guard) in tracked:
                        loops += 1
                        break
                    else:
                        tracked.add(tuple(guard))
            else:
                break

    return loops


def main():
    gd = parseInput(args.input)
    origin = gd.copy()

    # Part 1
    print(f"Part 1: {processData(gd)}")

    # Part 2
    print(f"Part 2: {processMore(origin)}")


if __name__ == "__main__":
    main()
