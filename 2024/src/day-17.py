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
    print("ADV: ", end="")
    registers["A"] = registers["A"] // (2 ** combo(arg))


def bxl(arg):
    print("BXL: ", end="")
    registers["B"] = registers["B"] ^ arg


def bst(arg):
    print("BST: ", end="")
    registers["B"] = combo(arg) % 8


def jnz(arg):
    print("JNZ: ", end="")
    if registers["A"] == 0:
        return None
    else:
        return arg


def bxc(arg):
    print("BXC: ", end="")
    registers["B"] = registers["B"] ^ registers["C"]


def out(arg):
    print("OUT: ", end="")
    output.append(combo(arg) % 8)


def bdv(arg):
    print("BDV: ", end="")
    registers["B"] = registers["A"] // (2 ** combo(arg))


def cdv(arg):
    print("CDV: ", end="")
    registers["C"] = registers["A"] // (2 ** combo(arg))


op = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]


# Run the 3-bit program
def processData():
    pnt = 0
    print(f"Executing: {instructions}")
    while pnt < len(instructions):
        print(f"Pnt: {pnt} - ({instructions[pnt]})")
        print(f"Reg: {registers} -> ", end="")
        if instructions[pnt] == 3:
            jump = op[instructions[pnt]](instructions[pnt+1])
            if jump is not None:
                pnt = jump
            else:
                pnt += 2
        else:
            op[instructions[pnt]](instructions[pnt+1])
            pnt += 2
        print(registers)
    return ",".join([str(x) for x in output])


# Process harder
def processMore():
    return False


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
