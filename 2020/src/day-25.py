#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Room Key.")
parser.add_argument('input', metavar='input', type=str,
                    help='Room key crypto input.')
args = parser.parse_args()

keys = []


def main():
    parseInput(args.input)

    # Part 1
    findHandshake()

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


# For the keys, identify its cycle and handshake
def findHandshake():
    subject = 7

    # Card
    value = 1
    loop = 0

    while value != keys[0]:
        value = (value * subject) % 20201227
        loop += 1

    print(loop)

    # Door
    value = 1
    loop = 0

    while value != keys[1]:
        value = (value * subject) % 20201227
        loop += 1

    print(loop)


def printKeys():
    for item in keys:
        print(item)


if __name__ == "__main__":
    main()
