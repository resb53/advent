#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

squares = []
rounds = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    maxx = 0
    y = 0
    for line in input_fh:
        line = line.rstrip()
        if maxx == 0:
            maxx = len(line)
        for x, val in enumerate(line):
            if val == "#":
                squares.append(complex(x, y))
            elif val == "O":
                rounds.append(complex(x, y))
        y += 1

    return (maxx, y)


# Tilt the deck
def tilt(direction, bounds):
    # Sort to focus on ones nearest the downward edge first
    match direction:
        case "N":
            rounds.sort(key=lambda x: x.imag)
            for i, pos in enumerate(rounds):
                nearObst = -1
                obstacles = [x for x in squares if x.real == pos.real]
                obstacles.extend([x for x in rounds if x.real == pos.real])
                for obs in obstacles:
                    if obs.imag < pos.imag and obs.imag > nearObst:
                        nearObst = obs.imag
                rounds[i] = complex(pos.real, nearObst + 1)

        case "E":
            rounds.sort(key=lambda x:x.real, reverse=True)
        case "S":
            rounds.sort(key=lambda x:x.imag, reverse=True)
        case "W":
            rounds.sort(key=lambda x:x.real)


# Print the grind
def printGrid(bounds):
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            pos = complex(x, y)
            if pos in squares:
                print("#", end="")
            elif pos in rounds:
                print("O", end="")
            else:
                print(".", end="")
        print()


# Calculate strain
def calculateStrain(bounds):
    strain = 0
    for x in rounds:
        strain += bounds[1] - x.imag
    return int(strain)


# Find the strain when all rocks moved North
def processData(bounds):
    # Tilt North
    tilt("N", bounds)
    return calculateStrain(bounds)


# Process harder
def processMore():
    return False


def main():
    bounds = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(bounds)}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
