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

    # Process packets
    done = False
    while hexpos < len(data) and not done:
        (ver, value, hexpos, bits) = processPacket(data, hexpos, bits)
        versum += ver
        # Check if it's only padding remaining
        if (bits.find("1") == -1) and (int(data[hexpos:], 16) == 0):
            done = True

    print(f"Solution to part 1: {versum}")


# Process a new packet
def processPacket(hexdata, next, bits):
    # Process headers
    ver = int(bits[0:3], 2)
    typ = int(bits[3:6], 2)

    # Send for futher processing
    if typ == 4:
        (value, next, bits) = convLiteral(hexdata, next, bits[6:])
    else:
        (value, next, bits, subversum) = convOperator(hexdata, next, bits[6:])
        ver += subversum

    return (ver, value, next, bits)


# Parse hex into binary representation
def convHex(hexdata, start, size):
    endpos = start+size
    data = hexdata[start:endpos]
    form = "0>" + str(size * 4) + "b"
    binrep = format(int(data, 16), form)
    return (binrep, endpos)


def convLiteral(hexdata, next, bits):
    done = False
    literal = ""
    while not done:
        while len(bits) < 5:
            (newbits, next) = convHex(hexdata, next, 1)
            bits += newbits
        if bits[0] == "0":
            done = True
        literal += bits[1:5]
        bits = bits[5:]

    return(int(literal, 2), next, bits)


def convOperator(hexdata, next, bits):
    mode = int(bits[0])
    bits = bits[1:]

    if mode == 0:
        subversum = 0

        while len(bits) < 15:
            (newbits, next) = convHex(hexdata, next, 1)
            bits += newbits
        subpacketlength = int(bits[0:15], 2)
        bits = bits[15:]

        while len(bits) < subpacketlength:
            (newbits, next) = convHex(hexdata, next, 1)
            bits += newbits
        subpacket = bits[0:subpacketlength]
        bits = bits[subpacketlength:]

        while (len(subpacket) > 0):
            (ver, value, next, subpacket) = processPacket(hexdata, next, subpacket)
            subversum += ver

    return (0, next, bits, subversum)


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
