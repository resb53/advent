#!/usr/bin/python3

import argparse
import sys
import re

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Bitmask.")
parser.add_argument('input', metavar='input', type=str,
                    help='Bitwise data input.')
args = parser.parse_args()

data = {}


class bit36:
    'Class for 36 bit unsigned integers'
    def __init__(self, val):
        if not isinstance(val, int):
            raise TypeError("Must be passed integer value.")
        if val < 0 or val > 68719476735:
            raise ValueError('Value initiated is outside bounds of 36-bit int.')

        self.bits = [0] * 36  # Most significant to least significant
        for i, v in enumerate('{0:036b}'.format(val)):
            self.bits[i] = v

    def setbit(self, i, v):
        self.bits[i] = v

    def __int__(self):
        return int(''.join(self.bits), 2)

    def __radd__(self, other):
        return other + int(self)

    def __repr__(self):
        return str(int(self))

    def __copy__(self):
        return bit36(int(self))


def main():
    # Part 1
    parseInput(args.input, 1)
    print(findInit())

    # Part 2
    parseInput(args.input, 2)
    print(findInit())

    # Debug
    # printData()


# Parse the input file
def parseInput(inp, version):
    global data
    data = {}
    mask = ['X'] * 36
    try:
        data_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in data_fh:
        match = re.match(r"^mem\[(\d+)\] = (\d+)$", line, re.I)
        if not match:
            mask = list(line.strip("\n").split(" = ")[1])
        else:
            mem = bit36(int(match.group(1)))
            val = bit36(int(match.group(2)))

            if version == 1:
                # Apply mask to val
                for i, v in enumerate(mask):
                    if v != 'X':
                        val.setbit(i, v)

                data[int(mem)] = val

            elif version == 2:
                dontcares = []

                # Apply mask to mem and set all 1's / find dontcares
                for i, v in enumerate(mask):
                    if v == '1':
                        mem.setbit(i, v)
                    elif v == 'X':
                        dontcares.append(i)

                # From dontcares identify list of affected memory
                options = getDCs(dontcares)

                # Add each address
                for opt in options:
                    bits = mem.bits.copy()

                    for i, v in enumerate(opt):
                        bits[dontcares[i]] = v

                    address = int(''.join(bits), 2)
                    data[address] = val


# Return list of lists of all don't care states
def getDCs(dcs):
    options = []

    total = 2 ** len(dcs)
    fmt = '{0:0'+str(len(dcs))+'b}'

    for i in range(total):
        options.append(list(fmt.format(i)))

    return options


# For each pass, identify its seat
def findInit():
    return sum(data.values())


def printData():
    for mem in data:
        print(f"{mem}: {data[mem]}")


if __name__ == "__main__":
    main()
