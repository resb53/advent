#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

segs = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}
univals = {
    2: 1,
    4: 4,
    3: 7,
    7: 8
}
poss = ["a", "b", "c", "d", "e", "f", "g"]
nums = []
outs = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        first, last = line.strip("\n").split(" | ")
        nums.append(first.split(" "))
        outs.append(last.split(" "))


# For each pass, identify unique values
def processEasy():
    uniques = 0
    for output in outs:
        for digit in output:
            if len(digit) in univals:
                uniques += 1

    print(f"Solution to part 1: {uniques}")


# Process harder
def processHard():
    totaloutput = 0

    for i, all in enumerate(nums):
        mapping = {}
        segments = {
            't': poss.copy(),
            'tl': poss.copy(),
            'tr': poss.copy(),
            'm': poss.copy(),
            'bl': poss.copy(),
            'br': poss.copy(),
            'b': poss.copy()
        }
        fivec = defaultdict(int)
        fives = []

        for val in all:
            # Get 1, 4, 7, 8
            if len(val) == 2:
                mapping[val] = 1
                for letter in val:
                    for p in ["t", "tl", "m", "bl", "b"]:
                        removePossibility(segments, p, letter)

            elif len(val) == 4:
                mapping[val] = 4
                for letter in val:
                    for p in ["t", "bl", "b"]:
                        removePossibility(segments, p, letter)

            elif len(val) == 3:
                mapping[val] = 7
                for letter in val:
                    for p in ["tl", "m", "bl", "b"]:
                        removePossibility(segments, p, letter)

            elif len(val) == 7:
                mapping[val] = 8

            # Analyse 5 length's (2, 3, 5)
            # t m b always in all 3
            # tl bl seen once
            elif len(val) == 5:
                fives.append(val)
                for letter in val:
                    fivec[letter] += 1

        # Act on 5s
        for letter in fivec:
            if fivec[letter] == 3:
                for p in ["tl", "tr", "bl", "br"]:
                    removePossibility(segments, p, letter)

        # We know bottom left
        for p in ["t", "tl", "tr", "m", "br", "b"]:
            removePossibility(segments, p, segments["bl"][0])

        # We know top left and bottom
        for p in ["t", "tr", "m", "br"]:
            removePossibility(segments, p, segments["tl"][0])
            removePossibility(segments, p, segments["b"][0])

        # Top right and Bottom right left - back to fives, use the two
        for val in fives:
            if segments["bl"][0] in val:
                two = list(val)
                for p in ["t", "m", "bl", "b"]:
                    two.remove(segments[p][0])
                segments["tr"] = [two[0]]
                removePossibility(segments, "br", segments["tr"][0])

        print(segments)


def removePossibility(segs, pos, value):
    try:
        segs[pos].remove(value)
    except ValueError:
        pass


def main():
    parseInput(args.input)

    # Part 1
    processEasy()

    # Part 2
    processHard()


if __name__ == "__main__":
    main()
