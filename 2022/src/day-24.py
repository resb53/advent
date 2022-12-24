#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

bounds = [0, 0]  # maxx, maxy
blizzs = []
winds = {
    ">": 1,
    "v": 1j,
    "<": -1,
    "^": -1j
}
elves = set([1])


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    row = 0

    for line in input_fh:
        line = line.strip("\n")
        bounds[0] = len(line)
        for i, x in enumerate(line):
            if x in winds:
                blizzs.append([i + row * 1j, winds[x]])
        row += 1

    bounds[1] = row


# Print the grid
def printGrid():
    # Prepare the grid
    crosswinds = defaultdict(list)
    for blizz in blizzs:
        crosswinds[blizz[0]].append(blizz[1])

    # Print the grid
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            pos = x + y * 1j
            if pos in elves:
                print("E", end="")
            elif pos == 1 or pos == (bounds[0] - 2) + (bounds[1] - 1) * 1j:
                print(".", end="")
            elif y == 0 or y == bounds[1] - 1 or x == 0 or x == bounds[0] - 1:
                print("#", end="")
            elif pos in crosswinds:
                if len(crosswinds[pos]) > 1:
                    print(len(crosswinds[pos]), end="")
                else:
                    print([k for k, v in winds.items() if v == crosswinds[pos][0]][0], end="")
            else:
                print(".", end="")
        print()


# Move the winds
def blowWinds():
    for blizz in blizzs:
        newpos = sum(blizz)
        if int(newpos.real) == 0:
            newpos += bounds[0] - 2
        elif int(newpos.imag) == 0:
            newpos += (bounds[1] - 2) * 1j
        elif int(newpos.real) == bounds[0] - 1:
            newpos -= bounds[0] - 2
        elif int(newpos.imag) == bounds[1] - 1:
            newpos -= (bounds[1] - 2) * 1j
        blizz[0] = newpos


# Move Elves
def moveElves():
    windpos = [x[0] for x in blizzs]
    global elves
    newelves = set()
    for elf in elves:
        newelves.update(availableMoves(elf, windpos))
    elves = newelves


# Find available moves
def availableMoves(pos, windpos):
    possible = [pos]
    possible.extend([pos + x for x in winds.values()])

    # Reverse order to pop from back without order changing
    for i in range(len(possible) - 1, -1, -1):
        x = int(possible[i].real)
        y = int(possible[i].imag)
        if (x == 1 and y == 0) or (x == (bounds[0] - 2) and y == (bounds[1] - 1)):
            continue
        elif y <= 0 or y >= bounds[1] - 1 or x <= 0 or x >= bounds[0] - 1:
            possible.pop(i)
        elif x + y * 1j in windpos:
            possible.pop(i)

    return possible


# Get from A to B avoiding the wind
def processData():
    goal = (bounds[0] - 2) + (bounds[1] - 1) * 1j
    minutes = 0

    while goal not in elves:
        minutes += 1
        blowWinds()
        moveElves()
        # printGrid()
        # _ = input()

    print(f"Part 1: {minutes}")

    return minutes


# Process going back and to the end again
def processMore(minutes):
    global elves
    elves = set([(bounds[0] - 2) + (bounds[1] - 1) * 1j])
    goal = 1

    while goal not in elves:
        minutes += 1
        blowWinds()
        moveElves()

    elves = set([1])
    goal = (bounds[0] - 2) + (bounds[1] - 1) * 1j

    while goal not in elves:
        minutes += 1
        blowWinds()
        moveElves()

    print(f"Part 2: {minutes}")


def main():
    parseInput(args.input)
    processMore(processData())


if __name__ == "__main__":
    main()
