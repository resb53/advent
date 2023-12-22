#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict
from random import choices
import string

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

stack = defaultdict(dict)
bricks = defaultdict(list)


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        start, finish = line.split("~")
        start = [int(x) for x in start.split(",")]
        finish = [int(x) for x in finish.split(",")]

        name = "".join(choices(string.ascii_uppercase + string.digits, k=3))
        if name in bricks or name + "v" in bricks:
            name = "".join(choices(string.ascii_uppercase + string.digits, k=3))

        # Find orientation
        for i in range(3):
            if start[i] != finish[i]:
                match i:
                    case 0:
                        for x in range(min((start[i], finish[i])), max((start[i], finish[i])) + 1):
                            stack[start[2]][complex(x, start[1])] = name
                            bricks[name].append((x, start[1], start[2]))
                    case 1:
                        for y in range(min((start[i], finish[i])), max((start[i], finish[i])) + 1):
                            stack[start[2]][complex(start[0], y)] = name
                            bricks[name].append((start[0], y, start[2]))
                    case 2:
                        for z in range(min((start[i], finish[i])), max((start[i], finish[i])) + 1):
                            stack[z][complex(start[0], start[1])] = name + "v"
                            bricks[name + "v"].append((start[0], start[1], z))


# Drop bricks like Tetris
def tetris():
    while True:
        drop = []
        for brick in bricks:
            droppable = True
            if brick[-1] == "v":
                if complex(bricks[brick][0][0], bricks[brick][0][1]) in stack[bricks[brick][0][2] - 1]:
                    droppable = False
            else:
                for pos in bricks[brick]:
                    if pos[2] == 1 or complex(pos[0], pos[1]) in stack[pos[2] - 1]:
                        droppable = False
            if droppable:
                drop.append(brick)

        if len(drop) == 0:
            return

        for brick in drop:
            newbrick = []
            for pos in bricks[brick]:
                newbrick.append((pos[0], pos[1], pos[2] - 1))
                stack[pos[2]].pop(complex(pos[0], pos[1]))
                stack[pos[2] - 1][complex(pos[0], pos[1])] = brick
            bricks[brick] = newbrick


# Identify number of bricks that can be safely disintegrated
def processData():
    tetris()
    return False


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
