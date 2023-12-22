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
                    case 2:  # Vertical
                        for z in range(min((start[i], finish[i])), max((start[i], finish[i])) + 1):
                            stack[z][complex(start[0], start[1])] = name + "v"
                            bricks[name + "v"].append((start[0], start[1], z))


# Drop bricks like Tetris
def tetris():
    # print(stack)
    ordered_bricks = list(bricks.keys())
    ordered_bricks.sort(key=lambda x: bricks[x][0][2])
    for brick in ordered_bricks:
        # print(f"{brick}: {bricks[brick]}")
        drop = 0
        if brick[-1] == "v":
            for z in range(bricks[brick][0][2] - 1, 0, -1):
                # print(f"Checking {(bricks[brick][0][0], bricks[brick][0][1], z)}...")
                if complex(bricks[brick][0][0], bricks[brick][0][1]) in stack[z]:
                    drop = bricks[brick][0][2] - z - 1
                    break
        else:
            for z in range(bricks[brick][0][2] - 1, 0, -1):
                for pos in bricks[brick]:
                    # print(f"Checking {(pos[0], pos[1], z)}...")
                    if complex(pos[0], pos[1]) in stack[z]:
                        drop = pos[2] - z - 1
                        break
                else:
                    continue
                break
        # print(f"Drop: {drop}")
        if drop > 0:
            newbrick = []
            for pos in bricks[brick]:
                newbrick.append((pos[0], pos[1], pos[2] - drop))
                stack[pos[2]].pop(complex(pos[0], pos[1]))
                stack[pos[2] - drop][complex(pos[0], pos[1])] = brick
            bricks[brick] = newbrick
            # print(f"Dropped to: {bricks[brick]}")


# Work through bricks to see if they are the only support for another. Return count of those that don't
def zappable():
    # print(stack)
    zap = 0
    for brick in bricks:
        # print(f"{brick}: {bricks[brick]}")
        if brick[-1] == "v":
            if complex(bricks[brick][-1][0], bricks[brick][-1][1]) not in stack[bricks[brick][-1][2] + 1]:
                zap += 1
        else:
            supporting = []
            for pos in bricks[brick]:
                if complex(pos[0], pos[1]) in stack[pos[2] + 1]:
                    supporting.append(stack[pos[2] + 1][complex(pos[0], pos[1])])
            if len(supporting) == 0:
                zap += 1
            else:
                # print(f"Supporting: {supporting}")
                zappable = True
                for suspended in supporting:
                    # print(f"{suspended} supported by: {getSupports(suspended)}")
                    if len(getSupports(suspended)) == 1:
                        zappable = False
                        break
                if zappable:
                    # print("Zap!")
                    zap += 1

    return zap


# Get supports for a given block
def getSupports(block):
    supports = []
    if block[-1] == "v":
        if complex(bricks[block][0][0], bricks[block][0][1]) in stack[bricks[block][0][2] - 1]:
            supports.append(stack[bricks[block][0][2] - 1][complex(bricks[block][0][0], bricks[block][0][1])])
    else:
        for pos in bricks[block]:
            if complex(pos[0], pos[1]) in stack[pos[2] - 1]:
                supports.append(stack[pos[2] - 1][complex(pos[0], pos[1])])
    return supports


# Identify number of bricks that can be safely disintegrated
def processData():
    tetris()
    return zappable()


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
