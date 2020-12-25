#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Room Key.")
parser.add_argument('input', metavar='input', type=str,
                    help='Room key crypto input.')
args = parser.parse_args()

keys = []
cycles = [17580934, 19976408]  # from findCycles()


def main():
    parseInput(args.input)

    # Part 1
    # findCycles()

    count = 0
    value = 1
    subject = keys[1]

    while count < cycles[0]:
        value = (value * subject) % 20201227
        count += 1

    print(value)


    # Part 2

    # Debug
    # printKeys()


# Parse the input file
def parseInput(inp):
    global keys
    try:
        keys_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in keys_fh:
        keys.append(int(line.strip("\n")))


# For the keys, identify their cycles
def findCycles():
    global cycles
    subject = 7

    # Card
    value = 1
    loop = 0

    while value != keys[0]:
        value = (value * subject) % 20201227
        loop += 1

    cycles.append(loop)

    # Door
    value = 1
    loop = 0

    while value != keys[1]:
        value = (value * subject) % 20201227
        loop += 1

    cycles.append(loop)


def printKeys():
    for item in keys:
        print(item)


if __name__ == "__main__":
    main()
