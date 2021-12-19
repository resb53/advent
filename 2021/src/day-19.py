#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict, Counter
from itertools import combinations

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

reports = defaultdict(list)
# All orientations relative to scanner 0
orientation = {0: 0}
offsets = {0: (0, 0, 0)}
done = []


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
def orientScanners():
    # For each beacon seen by scanner 0, compare to next scanner
    findOverlap(0)

    while len(orientation) < len(reports):
        nextup = None

        for i in orientation:
            if i not in done:
                nextup = i
                break

        findOverlap(nextup)


# Find overlaps with specified scanner
def findOverlap(scanner):
    for compare in range(len(reports)):
        if compare not in orientation:
            for orient, relposses in enumerate(rotateAxes(reports[compare])):
                checks = Counter()
                for base in reports[scanner]:
                    for relpos in relposses:
                        diff = (base[0] - relpos[0], base[1] - relpos[1], base[2] - relpos[2])
                        checks[diff] += 1
                for check in checks:
                    if checks[check] >= 12:
                        orientation[compare] = orient
                        offsets[compare] = (check[0] + offsets[scanner][0],
                                            check[1] + offsets[scanner][1],
                                            check[2] + offsets[scanner][2])
                        reports[compare] = relposses
    done.append(scanner)


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
        rotatedPos[1].append((pos[1], pos[0] * -1, pos[2]))
        rotatedPos[2].append((pos[0] * -1, pos[1] * -1, pos[2]))
        rotatedPos[3].append((pos[1] * -1, pos[0], pos[2]))

        rotatedPos[4].append((pos[0], pos[1] * -1, pos[2] * -1))
        rotatedPos[5].append((pos[1], pos[0], pos[2] * -1))
        rotatedPos[6].append((pos[0] * -1, pos[1], pos[2] * -1))
        rotatedPos[7].append((pos[1] * -1, pos[0] * -1, pos[2] * -1))

        rotatedPos[8].append((pos[0], pos[2], pos[1] * -1))
        rotatedPos[9].append((pos[1], pos[2], pos[0]))
        rotatedPos[10].append((pos[0] * -1, pos[2], pos[1]))
        rotatedPos[11].append((pos[1] * -1, pos[2], pos[0] * -1))

        rotatedPos[12].append((pos[0], pos[2] * -1, pos[1]))
        rotatedPos[13].append((pos[1], pos[2] * -1, pos[0] * -1))
        rotatedPos[14].append((pos[0] * -1, pos[2] * -1, pos[1] * -1))
        rotatedPos[15].append((pos[1] * -1, pos[2] * -1, pos[0]))

        rotatedPos[16].append((pos[2], pos[0], pos[1]))
        rotatedPos[17].append((pos[2], pos[1], pos[0] * -1))
        rotatedPos[18].append((pos[2], pos[0] * -1, pos[1] * -1))
        rotatedPos[19].append((pos[2], pos[1] * -1, pos[0]))

        rotatedPos[20].append((pos[2] * -1, pos[0], pos[1] * -1))
        rotatedPos[21].append((pos[2] * -1, pos[1], pos[0]))
        rotatedPos[22].append((pos[2] * -1, pos[0] * -1, pos[1]))
        rotatedPos[23].append((pos[2] * -1, pos[1] * -1, pos[0] * -1))

    return rotatedPos


# Translate each report to be relative position to scanner 0
def translateReports():
    for i in reports:
        newreport = []
        for pos in reports[i]:
            newreport.append(translate(pos, offsets[i]))
        reports[i] = newreport


# Translate a location
def translate(loc, diff):
    x = loc[0] + diff[0]
    y = loc[1] + diff[1]
    z = loc[2] + diff[2]
    return (x, y, z)


# Get set of beacons
def getBeacons():
    beacons = set()
    for scanner in reports:
        for pos in reports[scanner]:
            beacons.add(pos)

    return beacons


def manhattan(a, b):
    distance = 0
    distance += abs(a[0] - b[0])
    distance += abs(a[1] - b[1])
    distance += abs(a[2] - b[2])
    return distance


def main():
    parseInput(args.input)

    # Part 1
    orientScanners()
    translateReports()
    beacons = getBeacons()

    print(f"Solution to part 1: {len(beacons)}")

    # Part 2
    biggestdiff = 0

    for pairs in combinations(offsets.values(), 2):
        distance = manhattan(pairs[0], pairs[1])
        if distance > biggestdiff:
            biggestdiff = distance

    print(f"Solution to part 2: {biggestdiff}")


if __name__ == "__main__":
    main()
