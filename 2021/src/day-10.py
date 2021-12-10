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
completing = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
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
    score = 0
    completes = []
    for line in code:
        # First error found
        fef = False
        syntax = []
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
        # If no error found, check completeness
        if not fef:
            # print("Complete by adding ", end="")
            compscore = 0
            while len(syntax) > 0:
                # print(closing[syntax.pop()], end="")
                char = syntax.pop()
                compscore *= 5
                compscore += completing[closing[char]]
            # print("")
            completes.append(compscore)

    print(f"Solution to part 1: {score}")
    print(f"Solution to part 2: {sorted(completes)[int(len(completes)/2)]}")


# Process harder
def completeCheck():
    for line in code:
        if not code[line]:
            print(line)


def main():
    parseInput(args.input)

    # Part 1 and 2
    syntaxCheck()


if __name__ == "__main__":
    main()
