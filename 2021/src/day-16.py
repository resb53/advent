#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    data = input_fh.readline().strip("\n")

    return data


# For each pass, identify its seat
def processData(data):
    pos = 0
    # Take first two hex for headers
    while pos < len(data):
        (bits, pos) = convHex(data, pos, 2)
        print(bits)


# Parse hex into binary representation
def convHex(hex, start, size):
    endpos = start+size
    data = hex[start:endpos]
    form = "0>" + str(size * 4) + "b"
    binrep = format(int(data, 16), form)
    return (binrep, endpos)


# Process harder
def processMore():
    return False


def main():
    data = parseInput(args.input)

    # Part 1
    processData(data)

    # Part 2
    processMore()


if __name__ == "__main__":
    main()
