#!/usr/bin/python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Cubes.")
parser.add_argument('input', metavar='input', type=str,
                    help='Conway Cubes state input.')
args = parser.parse_args()

active = []  # x + to right, y + down, z + into
# Don't check ranges, just check neighbours of actives

# Array of neighbours
neighbs = []

for z in [-1, 0, 1]:
    for y in [-1, 0, 1]:
        for x in [-1, 0, 1]:
            neighbs.append([x, y, z])

neighbs.remove([0, 0, 0])


def main():
    parseInput(args.input)
    print("Before any cycles:")
    printActive()

    # Part 2
    cycleCubes(6)
    print(len(active))


# Parse the input file
def parseInput(inp):
    global active, xrange, yrange
    try:
        states_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y, z = 0, 0

    for line in states_fh:
        line = line.strip("\n")
        x = 0
        for cube in line:
            if cube == '#':
                active.append([x, y, z])
            x += 1
        y += 1

    xrange = [0, x]
    yrange = [0, y]


# For each pass, identify its seat
def cycleCubes(cycles):
    global active, xrange, yrange, zrange, wrange
    cycle = 0

    while cycle < cycles:
        # Calculate Changes
        toremove = []
        toappend = []

        # Count for all neighbour cubes
        neicount = defaultdict(int)  # Tuple of coords: active neighbours

        for calc in active:
            activeNeighbours(neicount, calc)

        for tnode in neicount.keys():
            lnode = list(tnode)
            if lnode in active:
                if neicount[tnode] != 2 and neicount[tnode] != 3:
                    toremove.append(lnode)

            else:
                if neicount[tnode] == 3:
                    toappend.append(lnode)

        # Update Actives
        for rem in toremove:
            active.remove(rem)
        for app in toappend:
            active.append(app)

        cycle += 1
        print(f"After {cycle} cycles:")
        printActive()


def activeNeighbours(neicount, calc):
    # Lots of overchecking in here - if I need more efficiency!
    for check in neighbs:
        bump = (calc[0] + check[0], calc[1] + check[1], calc[2] + check[2])
        neicount[bump] += 1


def printActive():
    xrange = [0, 0]
    yrange = [0, 0]
    zrange = [0, 0]

    for act in active:
        if act[0] < xrange[0]:
            xrange[0] = act[0]
        elif act[0] > xrange[1]:
            xrange[1] = act[0]

        elif act[1] < yrange[0]:
            yrange[0] = act[1]
        elif act[1] > yrange[1]:
            yrange[1] = act[1]

        elif act[2] < zrange[0]:
            zrange[0] = act[2]
        elif act[2] > zrange[1]:
            zrange[1] = act[2]

    for z in range(zrange[0], zrange[1]+1):
        print(f"z={z}")
        for y in range(yrange[0], yrange[1]+1):
            for x in range(xrange[0], xrange[1]+1):
                if [x, y, z] in active:
                    print('#', end='')
                else:
                    print('.', end='')
            print('')
        print('')


if __name__ == "__main__":
    main()
