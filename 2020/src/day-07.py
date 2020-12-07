#!/usr/bin/python3

import argparse
import sys
import re

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Bags.")
parser.add_argument('input', metavar='input', type=str,
                    help='Bag rule list input.')
args = parser.parse_args()

rules = []


def main():
    parseInput(args.input)

    # Part 1
    findBags()

    # Part 2

    # Debug
    printRules()


# Parse the input file
def parseInput(inp):
    global passes
    try:
        rules_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in rules_fh:
        line = line.strip("\n")
        match = re.match(r"^(\w+ \w+) bags contain (.+)\.$", line, re.I)
        if not match:
            print(f"Error: Can't parse {line}")
        else:
            container = match.group(1)
            contents = match.group(2)
            # print(f"Container: {container}, Contents: {contents}")


# For each pass, identify its seat
def findBags():
    return True


def printRules():
    for item in rules:
        print(item)


if __name__ == "__main__":
    main()
