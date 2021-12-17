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
    bits = ""
    value = None

    # Process packets
    done = False
    while not done:
        (ver, value, hexpos, bits) = processPacket(data, hexpos, bits)
        versum += ver
        # Check if it anything is remaining and if it is only padding
        if hexpos == len(data):
            done = True
        elif (bits.find("1") == -1) and (int(data[hexpos:], 16) == 0):
            done = True

    print(f"Solution to part 1: {versum}")
    print(f"Solution to part 2: {value}")


# Process a new packet
def processPacket(hexdata, next, bits):
    # Process headers (make sure at least 8 bits for safety)
    (bits, next) = getBits(hexdata, next, 8, bits)

    ver = int(bits[0:3], 2)
    typ = int(bits[3:6], 2)
    value = None

    # Send for futher processing
    if typ == 4:
        (value, next, bits) = convLiteral(hexdata, next, bits[6:])
    else:
        (values, next, bits, subversum) = convOperator(hexdata, next, bits[6:])
        ver += subversum

        if typ == 0:
            value = sum(values)
        elif typ == 1:
            value = values.pop(0)
            for val in values:
                value *= val
        elif typ == 2:
            value = min(values)
        elif typ == 3:
            value = max(values)
        elif typ == 5:
            value = int(values[0] > values[1])
        elif typ == 6:
            value = int(values[0] < values[1])
        elif typ == 7:
            value = int(values[0] == values[1])

    return (ver, value, next, bits)


# Add more bits by parsing hex into binary representation
def getBits(hexdata, next, size, bits):
    while len(bits) < size:
        data = hexdata[next:next+1]
        newbits = format(int(data, 16), "0>4b")
        bits += newbits
        next += 1

    return (bits, next)


def convLiteral(hexdata, next, bits):
    done = False
    literal = ""
    while not done:
        (bits, next) = getBits(hexdata, next, 5, bits)
        if bits[0] == "0":
            done = True
        literal += bits[1:5]
        bits = bits[5:]

    return(int(literal, 2), next, bits)


def convOperator(hexdata, next, bits):
    mode = int(bits[0])
    bits = bits[1:]
    subversum = 0
    subvalues = []

    if mode == 0:
        (bits, next) = getBits(hexdata, next, 15, bits)
        subpacketlength = int(bits[0:15], 2)
        bits = bits[15:]

        (bits, next) = getBits(hexdata, next, subpacketlength, bits)
        subpacket = bits[0:subpacketlength]
        bits = bits[subpacketlength:]

        while (len(subpacket) > 0):
            (ver, value, next, subpacket) = processPacket(hexdata, next, subpacket)
            subvalues.append(value)
            subversum += ver

    else:
        (bits, next) = getBits(hexdata, next, 11, bits)
        subpacketcount = int(bits[0:11], 2)
        bits = bits[11:]

        for _ in range(subpacketcount):
            (ver, value, next, bits) = processPacket(hexdata, next, bits)
            subvalues.append(value)
            subversum += ver

    return (subvalues, next, bits, subversum)


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
