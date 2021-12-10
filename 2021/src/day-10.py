#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

code = []
closing = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}
scoring = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        code.append(line.strip("\n"))


# For each pass, identify its seat
def syntaxCheck():
    syntax = []
    score = 0
    for line in code:
        # First error found
        fef = False
        for char in line:
            if char in ("(", "[", "{", "<"):
                syntax.append(char)
            else:
                check = syntax.pop()
                if char != closing[check]:
                    if not fef:
                        fef = char
                        # print(f"Expected {closing[check]}, but found {char} instead")
                        score += scoring[char]
    print(f"Solution to part 1: {score}")         


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    syntaxCheck()

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
