#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = {}
instr = []
bearing = {
    1: 0, 
    1j: 1,
    -1: 2,
    -1j: 3
}


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
                    data[i + row * 1j] = x
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


# Check Input
def printData():
    maxx = max([int(x.real) for x in data]) 
    maxy = max([int(y.imag) for y in data])
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if x + y * 1j in data:
                print(data[x + y * 1j], end="")
            else:
                print(" ", end="")
        print()

    print(instr)


# Move as per instruction
def moveAlong(state, cmd):
    if type(cmd) == int:
        for _ in range(cmd):
            if not unitMove(state):
                break


# Attempt to move one square
def unitMove(state):
    if sum(state) in data and data[sum(state)] == ".":
        state[0] = sum(state)
        return True
    else:
        return False


# Walk through the grid following the instructions
def processData():
    pos = min([int(x.real) for x in data if int(x.imag) == 0]) + 0j
    face = 1  # 1:R 1j:D -1:L -1j:U
    state = [pos, face]

    # for cmd in instr:
    moveAlong(state, instr[0])

    print(state)


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
