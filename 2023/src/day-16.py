#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

grid = {}
light = {}
bounds = []
compass = {
    "N": -1j,
    "E": 1,
    "S": 1j,
    "W": -1
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    for line in input_fh:
        line = line.rstrip()
        if len(bounds) == 0:
            bounds.append(len(line))
        for x, val in enumerate(line):
            pos = complex(x, y)
            grid[pos] = val
            light[pos] = ""
        y += 1
    bounds.append(y)


# Print a grid
def printLight():
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            pos = complex(x, y)
            if len(light[pos]) == 0:
                print(grid[pos], end="")
            elif len(light[pos]) == 1:
                print(light[pos], end="")
            else:
                print(len(light[pos]), end="")
        print()


# Propagate Light
def propagate(pos, dir):
    tar = pos + compass[dir]
    if tar.real > -1 and tar.real < bounds[0] and tar.imag > -1 and tar.imag < bounds[1]:
        match grid[tar]:
            case ".":
                if dir not in light[tar]:
                    light[tar] += dir
                    propagate(tar, dir)
            case "|":
                light[tar] = "X"
                if dir in "EW":
                    propagate(tar, "N")
                    propagate(tar, "S")
                else:
                    propagate(tar, dir)
            case "-":
                light[tar] = "X"
                if dir in "NS":
                    propagate(tar, "W")
                    propagate(tar, "E")
                else:
                    propagate(tar, dir)
            case "/":
                light[tar] = "X"
                if dir == "N":
                    propagate(tar, "E")
                elif dir == "E":
                    propagate(tar, "N")
                elif dir == "S":
                    propagate(tar, "W")
                elif dir == "W":
                    propagate(tar, "S")
            case "\\":
                light[tar] = "X"
                if dir == "N":
                    propagate(tar, "W")
                elif dir == "E":
                    propagate(tar, "S")
                elif dir == "S":
                    propagate(tar, "E")
                elif dir == "W":
                    propagate(tar, "N")


# Calculate the current light level
def lightLevel():
    strength = 0
    for lit in light.values():
        if len(lit) > 0:
            strength += 1
    return strength


# Follow the light through the grid
def processData():
    propagate(-1, "E")
    return lightLevel()


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
