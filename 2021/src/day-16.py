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
    versum = 0

    # Take first two hex for headers
    (bits, hexpos) = convHex(data, hexpos, 2)

    # Process headers
    ver = int(bits[0:3], 2)
    typ = int(bits[3:6], 2)
    # Update sum of versions
    versum += ver
    # Send for futher processing
    if typ == 4:
        (value, hexpos, bits) = convLiteral(data, hexpos, bits[6:])
        print(value)
    else:
        (value, hexpos, bits) = convOperator(data, hexpos, bits[6:])
        print(value)


# Process a new packet
def processPacket(hex, next, bits):
    # Process headers
    ver = int(bits[0:3], 2)
    typ = int(bits[3:6], 2)

    # Send for futher processing
    if typ == 4:
        (value, next, bits) = convLiteral(hex, next, bits[6:])
    else:
        (value, next, bits) = convOperator(hex, next, bits[6:])

    return (ver, value, next, bits)


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

    return(int(literal, 2), next, bits)


def convOperator(hex, next, bits):
    mode = int(bits[0])
    bits = bits[1:]

    if mode == 0:
        while len(bits) < 15:
            (newbits, next) = convHex(hex, next, 1)
            bits += newbits
        subpacketlength = int(bits[0:15], 2)
        bits = bits[15:]

        while len(bits) < subpacketlength:
            (newbits, next) = convHex(hex, next, 1)
            bits += newbits
        subpacket = bits[0:subpacketlength]
        bits = bits[subpacketlength:]

        while (len(subpacket) > 0):
            (ver, value, next, subpacket) = processPacket(hex, next, subpacket)
            #if subpacket.find("1") == -1:
            #    subpacket = ""
            print(f"V:{ver} -- {value} -- {subpacket}")

    return (0, next, bits)


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
