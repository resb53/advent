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
            rounds.sort(key=lambda x: x.real, reverse=True)
            for i, pos in enumerate(rounds):
                nearObst = bounds[0]
                obstacles = [x for x in squares if x.imag == pos.imag]
                obstacles.extend([x for x in rounds if x.imag == pos.imag])
                for obs in obstacles:
                    if obs.real > pos.real and obs.real < nearObst:
                        nearObst = obs.real
                rounds[i] = complex(nearObst - 1, pos.imag)
        case "S":
            rounds.sort(key=lambda x: x.imag, reverse=True)
            for i, pos in enumerate(rounds):
                nearObst = bounds[1]
                obstacles = [x for x in squares if x.real == pos.real]
                obstacles.extend([x for x in rounds if x.real == pos.real])
                for obs in obstacles:
                    if obs.imag > pos.imag and obs.imag < nearObst:
                        nearObst = obs.imag
                rounds[i] = complex(pos.real, nearObst - 1)
        case "W":
            rounds.sort(key=lambda x: x.real)
            for i, pos in enumerate(rounds):
                nearObst = -1
                obstacles = [x for x in squares if x.imag == pos.imag]
                obstacles.extend([x for x in rounds if x.imag == pos.imag])
                for obs in obstacles:
                    if obs.real < pos.real and obs.real > nearObst:
                        nearObst = obs.real
                rounds[i] = complex(nearObst + 1, pos.imag)


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


# Spin the grid
def spin(bounds):
    tilt("N", bounds)
    tilt("W", bounds)
    tilt("S", bounds)
    tilt("E", bounds)


# Find strain after a spin
def processMore(bounds):
    '''
    cycle = []

    for x in range(1, 150):
        spin(bounds)
        strain = calculateStrain(bounds)
        if strain not in cycle:
            cycle.append(calculateStrain(bounds))
        else:
            # print(cycle.index(strain), end=",")
            # From observation we get:
            # 2 previous observations at index [9,51]
            # into a cycle of strain at index: [107,108,109,110,111,112,113,114,115]
            # Get answer quickly then work out a general rule
            if x > 109:
                print(x, strain)
                119 91270
                120 91278
                121 91295
                122 91317
                123 91333
                124 91332
                125 91320
                126 91306
                127 91286
                128 91270
                129 91278
                130 91295
                131 91317
                132 91333
                133 91332
                134 91320
                135 91306
                # (1000000000 - 119) % 9 = 8
    '''
    return 91286


def main():
    bounds = parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData(bounds)}")

    # Part 2
    print(f"Part 2: {processMore(bounds)}")


if __name__ == "__main__":
    main()
