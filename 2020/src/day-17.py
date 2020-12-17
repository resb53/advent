#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Cubes.")
parser.add_argument('input', metavar='input', type=str,
                    help='Conway Cubes state input.')
args = parser.parse_args()

active = []  # x + to right, y + down, z + into
xrange = [0, 1]
yrange = [0, 1]
zrange = [0, 1]  # Range maxes +1 for use of range() function
# Array of neighbours
neighbs = [
        [-1, -1, -1], [ 0, -1, -1], [ 1, -1, -1],
        [-1,  0, -1], [ 0,  0, -1], [ 1,  0, -1],
        [-1,  1, -1], [ 0,  1, -1], [ 1,  1, -1],
        [-1, -1,  0], [ 0, -1,  0], [ 1, -1,  0],
        [-1,  0,  0],               [ 1,  0,  0],
        [-1,  1,  0], [ 0,  1,  0], [ 1,  1,  0],
        [-1, -1,  1], [ 0, -1,  1], [ 1, -1,  1],
        [-1,  0,  1], [ 0,  0,  1], [ 1,  0,  1],
        [-1,  1,  1], [ 0,  1,  1], [ 1,  1,  1],
    ]


def main():
    parseInput(args.input)
    # print("Before any cycles:")
    # printActive()

    # Part 1
    cycleCubes(6)
    print(len(active))

    # Part 2

    # Debug
    # printActive()
    # print(xrange)
    # print(yrange)


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
    global active, xrange, yrange, zrange
    cycle = 0

    while cycle < cycles:
        # Calculate Changes
        toremove = []
        toappend = []

        for z in range(zrange[0]-1, zrange[1]+1):
            for y in range(yrange[0]-1, yrange[1]+1):
                for x in range(xrange[0]-1, xrange[1]+1):
                    count = activeNeighbours(x, y, z)

                    if [x, y, z] in active:
                        if count != 2 and count != 3:
                            toremove.append([x, y, z])
                            # active.remove([x, y, z])
                    else:
                        if count == 3:
                            toappend.append([x, y, z])
                            # active.append([x, y, z])

        # Update Actives
        for rem in toremove:
            active.remove(rem)
        for app in toappend:
            active.append(app)

        # Update Ranges
        for act in active:
            if act[0] < xrange[0]:
                xrange[0] = act[0]
            elif act[0]+1 > xrange[1]:
                xrange[1] = act[0]+1
            elif act[1] < yrange[0]:
                yrange[0] = act[1]
            elif act[1]+1 > yrange[1]:
                yrange[1] = act[1]+1
            elif act[2] < zrange[0]:
                zrange[0] = act[2]
            elif act[2]+1 > zrange[1]:
                zrange[1] = act[2]+1

        cycle += 1
        # print(f"After {cycle} cycles:")
        # printActive()


def activeNeighbours(x, y, z):
    count = 0
    # Lost of overchecking in here - if I need more efficiency!
    for check in neighbs:
        if [x + check[0], y + check[1], z + check[2]] in active:
            count += 1

    return count


def printActive():
    for z in range(zrange[0], zrange[1]):
        print(f"z={z}: ({xrange}, {yrange}, {zrange})")
        for y in range(yrange[0], yrange[1]):
            for x in range(xrange[0], xrange[1]):
                if [x, y, z] in active:
                    print('#', end='')
                else:
                    print('.', end='')
            print('')
        print('')


if __name__ == "__main__":
    main()
