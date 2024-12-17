#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

registers = {}
instructions = []
output = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        line = line.rstrip()
        if len(line) > 0:
            if line[0:8] == "Register":
                reg = line[9]
                val = int(line[12:])
                registers[reg] = val
            elif line[0:7] == "Program":
                instructions.extend([int(x) for x in line[9:].split(",")])


# Combo operand
def combo(val):
    if val in range(0, 4):
        return val
    elif val == 4:
        return registers["A"]
    elif val == 5:
        return registers["B"]
    elif val == 6:
        return registers["C"]
    else:
        sys.exit(f"Invalid combo operand called: {val}")


# Begin instructions
def adv(arg):
    registers["A"] = registers["A"] // (2 ** combo(arg))


def bxl(arg):
    registers["B"] = registers["B"] ^ arg


def bst(arg):
    registers["B"] = combo(arg) % 8


def jnz(arg):
    if registers["A"] == 0:
        return None
    else:
        return arg


def bxc(arg):
    registers["B"] = registers["B"] ^ registers["C"]


def out(arg):
    output.append(combo(arg) % 8)


def bdv(arg):
    registers["B"] = registers["A"] // (2 ** combo(arg))


def cdv(arg):
    registers["C"] = registers["A"] // (2 ** combo(arg))


op = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]


# Run the 3-bit program
def runInstructions():
    pnt = 0
    while pnt < len(instructions):
        if instructions[pnt] == 3:
            jump = op[instructions[pnt]](instructions[pnt+1])
            if jump is not None:
                pnt = jump
            else:
                pnt += 2
        else:
            op[instructions[pnt]](instructions[pnt+1])
            pnt += 2


# Find proper initialisation for A

# Big steps through each digit, getting smaller as we close in on the true value.
# 1 digit: 1st: 1, Step: 1, End: 7
# 2 digit: 1st: 8, Step: 8, End: 63
# 3 digit: 1st: 64, Step: 64, End: 511
# 4 digit: 1st: 512, etc -- Octals!

def findRegister():
    #     1111111
    #     6543210987654321
    a = 0o1000000000000000
    inc = 15  # **8

    for x in range(a, 8**(inc+1), 8**inc):
        registers["A"] = x
        registers["B"] = 0
        registers["C"] = 0
        output.clear()
        runInstructions()

        if output[inc] == instructions[inc]:
            stepThrough(x, inc-1)


# Recursively increment next most significant figure
def stepThrough(start, inc):
    matches = []
    for x in range(start, start + 8**(inc+1), 8**inc):
        registers["A"] = x
        registers["B"] = 0
        registers["C"] = 0
        output.clear()
        runInstructions()

        if output[inc] == instructions[inc]:
            matches.append(x)

    if inc > 0:
        for option in matches:
            stepThrough(option, inc-1)
    else:
        print(f"Part 2: {min(matches)}")


def main():
    parseInput(args.input)

    # Part 1
    runInstructions()
    print(f"Part 1: {",".join([str(x) for x in output])}")

    # Part 2
    findRegister()


if __name__ == "__main__":
    main()
