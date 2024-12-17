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
def processData():
    pnt = 0
    print(f"Executing: {instructions}")
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
    return ",".join([str(x) for x in output])


# Find proper initialisation for A
def processMore():
    a = -1
    success = False
    while True:
        if success:
            if len(output) == len(instructions):
                match = True
                for i in range(len(instructions)):
                    if output[i] != instructions[i]:
                        match = False
                        break
                if match:
                    return a
        # Try next
        a += 1
        pnt = 0
        print(f"Testing with A={a}", end="\r")
        registers["A"] = a
        registers["B"] = 0
        registers["C"] = 0
        output.clear()

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
            success = True
            if len(output) > len(instructions):
                success = False
                break


def main():
    parseInput(args.input)

    # Part 1
    print(f"Part 1: {processData()}")

    # Part 2
    print(f"Part 2: {processMore()}")


if __name__ == "__main__":
    main()
