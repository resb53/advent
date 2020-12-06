#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Customs Forms.")
parser.add_argument('input', metavar='input', type=str,
                    help='Customs group form input.')
args = parser.parse_args()

forms = []


def main():
    parseInput(args.input)

    # Part 1
    print(findTicks())

    # Part 2
    print(findAllTicked())

    # Debug
    # printForms()


# Parse the input file
def parseInput(inp):
    global forms
    try:
        customs_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    group = []

    for line in customs_fh:
        line = line.strip("\n")

        if line == '':
            forms.append(group)
            group = []

        else:
            group.append(line)

    forms.append(group)


# For each group, identify its ticked questions
def findTicks():
    sumall = 0

    for group in forms:
        ticks = {}

        for response in group:
            for tick in response:
                if tick in ticks:
                    ticks[tick] = ticks[tick] + 1
                else:
                    ticks[tick] = 1

        sumall += len(ticks)

    return sumall


# For each group identify questions the whole group ticked
def findAllTicked():
    sumall = 0

    for group in forms:
        ticks = {}
        size = len(group)

        for response in group:
            for tick in response:
                if tick in ticks:
                    ticks[tick] = ticks[tick] + 1
                else:
                    ticks[tick] = 1

        for question in ticks:
            if ticks[question] == size:
                sumall += 1

    return sumall


def printForms():
    for item in forms:
        print(item)


if __name__ == "__main__":
    main()
