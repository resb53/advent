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
    hexpos = 0
    # Take first two hex for headers
    (bits, hexpos) = convHex(data, hexpos, 2)
    # Process headers
    ver = int(bits[0:3], 2)
    typ = int(bits[3:6], 2)
    # Send for futher processing
    if typ == 4:
        (value, hexpos) = convLiteral(data, hexpos, bits[6:])
        print(value)


# Parse hex into binary representation
def convHex(hex, start, size):
    endpos = start+size
    data = hex[start:endpos]
    form = "0>" + str(size * 4) + "b"
    binrep = format(int(data, 16), form)
    return (binrep, endpos)


def convLiteral(hex, next, bits):
    done = False
    literal = ""
    while not done:
        while len(bits) < 5:
            (newbits, next) = convHex(hex, next, 1)
            bits += newbits
        if bits[0] == "0":
            done = True
        literal += bits[1:5]
        bits = bits[5:]

    return(int(literal, 2), next)


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
