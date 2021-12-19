#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict, Counter

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

reports = defaultdict(list)
# All orientations relative to scanner 0
orientation = {0: 0}
position = {0: (0, 0, 0)}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    scanner = None

    for line in input_fh:
        line = line.strip("\n")
        if line[0:3] == "---":
            scanner = int(line.split(" ")[2])
        elif len(line) == 0:
            continue
        else:           
            (x, y, z) = line.split(",")
            reports[scanner].append((int(x), int(y), int(z)))


# For each pass, identify its seat
def findOverlap():
    # For each beacon seen by scanner 0, compare to next scanner
    for orient, relposses in enumerate(rotateAxes(reports[1])):
        checks = Counter()
        for compare in reports[0]:
            for relpos in relposses:
                diff = (compare[0] - relpos[0], compare[1] - relpos[1], compare[2] - relpos[2])
                checks[diff] += 1
        for check in checks:
            if checks[check] >= 12:
                orientation[1] = orient
                position[1] = check

    print(orientation)
    print(position)


# Translate a location
def translate(loc, diff):
    x = loc[0] + diff[0]
    y = loc[1] + diff[1]
    z = loc[2] + diff[2]
    return (x, y, z)


# Rotate axes
def rotateAxes(locs):
    rotatedPos = [
        [], [], [], [], [], [],
        [], [], [], [], [], [],
        [], [], [], [], [], [],
        [], [], [], [], [], []
    ]
    for pos in locs:
        rotatedPos[0].append(pos)
        rotatedPos[1].append((pos[1]     , pos[0] * -1, pos[2]     ))
        rotatedPos[2].append((pos[0] * -1, pos[1] * -1, pos[2]     ))
        rotatedPos[3].append((pos[1] * -1, pos[0]     , pos[2]     ))

        rotatedPos[4].append((pos[0]     , pos[1] * -1, pos[2] * -1))
        rotatedPos[5].append((pos[1]     , pos[0]     , pos[2] * -1))
        rotatedPos[6].append((pos[0] * -1, pos[1]     , pos[2] * -1))
        rotatedPos[7].append((pos[1] * -1, pos[0] * -1, pos[2] * -1))

        rotatedPos[8].append((pos[0]     , pos[2]     , pos[1] * -1))
        rotatedPos[9].append((pos[1]     , pos[2]     , pos[0]     ))
        rotatedPos[10].append((pos[0] * -1, pos[2]     , pos[1]     ))
        rotatedPos[11].append((pos[1] * -1, pos[2]     , pos[0] * -1))

        rotatedPos[12].append((pos[0]     , pos[2] * -1, pos[1]     ))
        rotatedPos[13].append((pos[1]     , pos[2] * -1, pos[0] * -1))
        rotatedPos[14].append((pos[0] * -1, pos[2] * -1, pos[1] * -1))
        rotatedPos[15].append((pos[1] * -1, pos[2] * -1, pos[0]     ))

        rotatedPos[16].append((pos[2]     , pos[0]     , pos[1]     ))
        rotatedPos[17].append((pos[2]     , pos[1]     , pos[0] * -1))
        rotatedPos[18].append((pos[2]     , pos[0] * -1, pos[1] * -1))
        rotatedPos[19].append((pos[2]     , pos[1] * -1, pos[0]     ))

        rotatedPos[20].append((pos[2] * -1, pos[0]     , pos[1] * -1))
        rotatedPos[21].append((pos[2] * -1, pos[1]     , pos[0]     ))
        rotatedPos[22].append((pos[2] * -1, pos[0] * -1, pos[1]     ))
        rotatedPos[23].append((pos[2] * -1, pos[1] * -1, pos[0] * -1))

    return rotatedPos


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    findOverlap()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
