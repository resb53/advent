#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

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
            if len(digit) in [2, 3, 4, 7]:
                uniques += 1

    print(f"Solution to part 1: {uniques}")


def removePossibility(segs, pos, value):
    try:
        segs[pos].remove(value)
    except ValueError:
        pass


# Process harder
def processHard():
    totaloutput = 0

    for i, all in enumerate(nums):
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
            # Get 1, 4, 7, (8)
            if len(val) == 2:
                for letter in val:
                    for p in ["t", "tl", "m", "bl", "b"]:
                        removePossibility(segments, p, letter)

            elif len(val) == 4:
                for letter in val:
                    for p in ["t", "bl", "b"]:
                        removePossibility(segments, p, letter)

            elif len(val) == 3:
                for letter in val:
                    for p in ["tl", "m", "bl", "b"]:
                        removePossibility(segments, p, letter)

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

        rev = {}
        for x in segments:
            rev[segments[x][0]] = x

        # Segments found! Analyse output
        output = ""
        for num in outs[i]:
            light = []
            for x in num:
                light.append(rev[x])

            if len(light) == 2:
                output += "1"
            elif len(light) == 4:
                output += "4"
            elif len(light) == 3:
                output += "7"
            elif len(light) == 7:
                output += "8"
            elif len(light) == 5:
                if "bl" in light:
                    output += "2"
                elif "tl" in light:
                    output += "5"
                else:
                    output += "3"
            elif len(light) == 6:
                if "m" not in light:
                    output += "0"
                elif "tr" not in light:
                    output += "6"
                else:
                    output += "9"
            else:
                sys.exit("ERROR WITH LIGHTS!")

        totaloutput += int(output)

    print(f"Solution to part 2: {totaloutput}")


def main():
    parseInput(args.input)

    # Part 1
    processEasy()

    # Part 2
    processHard()


if __name__ == "__main__":
    main()
