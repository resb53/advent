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
maxx = 0
maxy = 0


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    global maxx, maxy
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

    maxx = max([int(x.real) for x in grid])
    maxy = max([int(y.imag) for y in grid])


# Check Input
def printGrid():
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if x + y * 1j in grid:
                print(grid[x + y * 1j], end="")
            else:
                print(" ", end="")
        print()


# Move as per instruction
def moveAlong(state, cmd, part):
    if type(cmd) == int:
        for _ in range(cmd):
            if not unitMove(state, part):
                break

    elif cmd == "R":
        state[1].rotate(-1)
    elif cmd == "L":
        state[1].rotate(1)


# Attempt to move one square
def unitMove(state, part):
    target = state[0] + state[1][0]
    rot = None
    if target not in grid:
        if part == 1:
            target, rot = wrapPos(state)
        else:
            target, rot = foldPos(state)

    try:
        if grid[target] == ".":
            state[0] = target
            if rot is not None:
                state[1].rotate(rot)
            return True
        else:
            return False
    except KeyError as e:
        sys.exit(f"{state[0]}: {e}")


# Find wrapped target (Part 1)
def wrapPos(state):
    if state[1][0] == 1:
        return min([int(x.real) for x in grid if int(x.imag) == int(state[0].imag)]) + int(state[0].imag) * 1j, None
    elif state[1][0] == 1j:
        return int(state[0].real) + min([int(x.imag) for x in grid if int(x.real) == int(state[0].real)]) * 1j, None
    elif state[1][0] == -1:
        return max([int(x.real) for x in grid if int(x.imag) == int(state[0].imag)]) + int(state[0].imag) * 1j, None
    elif state[1][0] == -1j:
        return int(state[0].real) + max([int(x.imag) for x in grid if int(x.real) == int(state[0].real)]) * 1j, None


# Find folded target (Part 2 - hardcode side positions, not general solution)
def foldPos(state):
    '''
    Example sides(4):   Real input sides(50):
        1                     1 2
    2 3 4                     3
        5 6                 4 5
                            6
    '''
    x = int(state[0].real)
    y = int(state[0].imag)

    # Move and turn depending on edge
    '''
    # Test data
    # Top 1 to top 2
    if x in range(8, 12) and y == 0:
        pos = (11 - x) + 4j
        rot = 2
    elif x in range(0, 4) and y == 4:
        pos = (11 - x) + 0j
        rot = 2
    # Right 1 to right 6
    elif x == 11 and y in range(0, 4):
        pos = 15 + (11 - y) * 1j
        rot = 2
    elif x == 15 and y in range(8, 12):
        pos = 11 + (11 - y) * 1j
        rot = 2
    # Right 4 to top 6
    elif x == 11 and y in range(4, 8):
        pos = (19 - y) + 8j
        rot = -1
    elif x in range(12, 16) and y == 8:
        pos = 11 + (19 - x) * 1j
        rot = 1
    # Bottom 6 to left 2
    elif x in range(12, 16) and y == 11:
        pos = 0 + (19 - x) * 1j
        rot = 1
    elif x == 0 and y in range(4, 8):
        pos = (19 - x) + 11j
        rot = -1
    # Bottom 5 to bottom 2
    elif x in range(8, 12) and y == 11:
        pos = (11 - x) + 7j
        rot = 2
    elif x in range(0, 4) and y == 7:
        pos = (11 - x) + 11j
        rot = 2
    # Left 5 to bottom 3
    elif x == 8 and y in range(8, 12):
        pos = (15 - y) + 7j
        rot = -1
    elif x in range(4, 8) and y == 7:
        pos = 8 + (15 - x) * 1j
        rot = 1
    # Top 3 to left 1
    elif x in range(4, 8) and y == 4:
        pos = 8 + (x - 4) * 1j
        rot = -1
    elif x == 8 and y in range(0, 4):
        pos = (y + 4) + 4j
        rot = 1
    else:
        sys.exit(f"Fail: {state}")
    '''

    # Top 1 to left 6
    if x in range(50, 100) and y == 0:
        pos = 0 + (100 + x) * 1j
        rot = -1
    elif x == 0 and y in range(150, 200):
        pos = (y - 100) + 0j
        rot = 1
    # Top 2 to bottom 6
    elif x in range(100, 150) and y == 0:
        pos = (x - 100) + 199j
        rot = 0
    elif x in range(0, 50) and y == 199:
        pos = (x + 100) + 0j
        rot = 0
    # Right 2 to right 5
    elif x == 149 and y in range(0, 50):
        pos = 99 + (149 - y) * 1j
        rot = 2
    elif x == 99 and y in range(100, 149):
        pos = 149 + (149 - y) * 1j
        rot = 2
    # Bottom 2 to right 3
    elif x in range(100, 150) and y == 49:
        pos = 99 + (x - 50) * 1j
        rot = -1
    elif x == 99 and y in range(50, 100):
        pos = (y + 50) + 49j
        rot = 1
    # Bottom 5 to right 6
    elif x in range(50, 100) and y == 149:
        pos = 49 + (x + 100) * 1j
        rot = -1
    elif x == 49 and y in range(150, 200):
        pos = (y - 100) + 149j
        rot = 1
    # Left 4 to left 1
    elif x == 0 and y in range(100, 150):
        pos = 50 + (149 - y) * 1j
        rot = 2
    elif x == 50 and y in range(0, 50):
        pos = 0 + (149 - y) * 1j
        rot = 2
    # Top 4 to left 3
    elif x in range(0, 50) and y == 100:
        pos = 50 + (x + 50) * 1j
        rot = -1
    elif x == 50 and y in range(50, 100):
        pos = (y - 50) + 100j
        rot = 1
    else:
        sys.exit(f"Fail: {state}")

    return pos, rot


# Walk through the grid following the instructions
def processData(part):
    pos = min([int(x.real) for x in grid if int(x.imag) == 0]) + 0j
    state = [pos, face]

    for cmd in instr:
        moveAlong(state, cmd, part)

    print(f"Part {part}: {(int(state[0].imag) + 1) * 1000 + (int(state[0].real) + 1) * 4 + bearing[state[1][0]]}")


def main():
    parseInput(args.input)

    # Part 1}
    processData(1)

    # Part 2
    processData(2)


if __name__ == "__main__":
    main()
