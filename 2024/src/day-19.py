#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []
options = {}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    t = True
    for line in input_fh:
        line = line.rstrip()
        if len(line) == 0:
            t = False
        elif t:
            towels = line.split(", ")
        else:
            data.append(line)

    for towel in towels:
        base = options
        for char in towel:
            if char not in base:
                base[char] = {}
            base = base[char]
        base["."] = "."


# Identify if it's possible to make each pattern from the towels
# Alternatively, drop this approach entirely and just concatenante strings, may be better.
def processData():
    possible = 0
    for pattern in data:
        print(f"Checking {pattern}", end="")
        combinations = []
        addNewTowel(list(pattern), [], combinations)
        if len(combinations) > 0:
            possible += 1
            print(" ✓")
        else:
            print(" ✗")
    return possible


def addNewTowel(pattern, explore, combs):
    pattern = pattern.copy()
    explore = explore.copy()
    if pattern[0] in options:
        char = pattern.pop(0)
        explore.append(char)
        extendPattern(pattern, options[char], explore, combs)


def extendPattern(pattern, base, explore, combs):
    if len(pattern) == 0 and "." in base:
        combs.append(explore)
    elif len(pattern) > 0:
        if "." in base:
            if len(pattern) > 0:
                addNewTowel(pattern, explore, combs)
        if pattern[0] in base:
            char = pattern.pop(0)
            explore[-1] += char
            extendPattern(pattern, base[char], explore, combs)


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
