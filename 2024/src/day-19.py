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
def processData():
    possible = 0
    for pattern in data:
        print(f"Pattern: {pattern}")
        if pattern[0] in options:
            combinations = [[]]
            # Pattern, char in pattern, base, possible combinations, current combination
            createPattern(pattern, 1, options[pattern[0]], combinations, 0)
            if len(combinations) > 0:
                possible += 1
    return possible


# For a pattern iterate through options recursively
def createPattern(pattern, i, base, combs, c):
    print(f"Create: {(pattern, i, base.keys())}")
    if i > len(pattern) - 1:
        if "." in base:
            return

    char = pattern[i]
    print(f"Char: {char}")
    if "." in base:
        # Start a new towel
        if char in options:
            combs[c].append("char")
            createPattern(pattern, i, options[char], combs, c)
    if char in base:
        createPattern(pattern, i + 1, base[char], combs)
    else:
        return


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
