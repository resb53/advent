#!/usr/bin/env python3

import argparse
import sys
from collections import deque

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
instr = []
bearing = {
    1: 0,
    1j: 1,
    -1: 2,
    -1j: 3
}
face = deque(bearing.keys())


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    row = 0
    for line in input_fh:
        line = line.strip("\n")
        if line.startswith(" ") or line.startswith(".") or line.startswith("#"):
            for i, x in enumerate(line):
                if x == "." or x == "#":
                    grid[i + row * 1j] = x
            row += 1
        elif len(line) > 0:
            current = ""
            for x in line:
                if x != "R" and x != "L":
                    current += x
                else:
                    instr.append(int(current))
                    current = ""
                    instr.append(x)
            instr.append(int(current))


# Check Input
def printGrid():
    maxx = max([int(x.real) for x in grid])
    maxy = max([int(y.imag) for y in grid])
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if x + y * 1j in grid:
                print(grid[x + y * 1j], end="")
            else:
                print(" ", end="")
        print()


# Move as per instruction
def moveAlong(state, cmd):
    if type(cmd) == int:
        for _ in range(cmd):
            if not unitMove(state):
                break

    elif cmd == "R":
        state[1].rotate(-1)
    elif cmd == "L":
        state[1].rotate(1)


# Attempt to move one square
def unitMove(state):
    target = state[0] + state[1][0]
    if target not in grid:
        target = wrapPos(state)

    if grid[target] == ".":
        state[0] = target
        return True
    else:
        return False


# Find wrapped target
def wrapPos(state):
    if state[1][0] == 1:
        return min([int(x.real) for x in grid if int(x.imag) == int(state[0].imag)]) + int(state[0].imag) * 1j
    elif state[1][0] == 1j:
        return int(state[0].real) + min([int(x.imag) for x in grid if int(x.real) == int(state[0].real)]) * 1j
    elif state[1][0] == -1:
        return max([int(x.real) for x in grid if int(x.imag) == int(state[0].imag)]) + int(state[0].imag) * 1j
    elif state[1][0] == -1j:
        return int(state[0].real) + max([int(x.imag) for x in grid if int(x.real) == int(state[0].real)]) * 1j


# Walk through the grid following the instructions
def processData():
    pos = min([int(x.real) for x in grid if int(x.imag) == 0]) + 0j
    state = [pos, face]

    for cmd in instr:
        moveAlong(state, cmd)

    print(f"Part 1: {(int(state[0].imag) + 1) * 1000 + (int(state[0].real) + 1) * 4 + bearing[state[1][0]]}")


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1}
    processData()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
