#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        data.extend(line.rstrip().split(","))


# Calculate hash of a string
def strhash(string):
    strhash = 0
    for c in string:
        strhash += ord(c)
        strhash *= 17
        strhash %= 256

    return strhash


# Sum the hashes of the lines
def processData():
    hashsum = 0
    for x in data:
        hashsum += strhash(x)
    return hashsum


# Insert the lenses using HASHMAP
def processMore():
    boxes = [[] for _ in range(256)]
    for x in data:
        if "-" in x:
            remove = None
            label = x[:-1]
            boxid = strhash(label)
            for j, lens in enumerate(boxes[boxid]):
                if lens[0] == label:
                    remove = j
            if remove is not None:
                boxes[boxid].pop(remove)
        else:
            replace = None
            label, value = x.split("=")
            boxid = strhash(label)
            for j, lens in enumerate(boxes[boxid]):
                if lens[0] == label:
                    replace = j
            if replace is not None:
                boxes[boxid][replace][1] = int(value)
            else:
                boxes[boxid].append([label, int(value)])

    # Calculate focussing power
    power = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            p = (i + 1) * (j + 1) * lens[1]
            power += p
    return power


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
