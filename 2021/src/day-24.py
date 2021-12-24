#!/usr/bin/env python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

vars = ["w", "x", "y", "z"]

# Parse the input file
def parseInput(inp):
    instr = []

    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        args = line.strip("\n").split(" ")
        if len(args) > 2:
            if args[2] not in vars:
                args[2] = int(args[2])
        instr.append(args)

    return instr


def doinp(reg, v, a):
    reg[v] = a


def doadd(reg, a, b):
    if type(b) == int:
        reg[a] = reg[a] + b
    else:
        reg[a] = reg[a] + reg[b]


def domul(reg, a, b):
    if type(b) == int:
        reg[a] = reg[a] * b
    else:
        reg[a] = reg[a] * reg[b]


def dodiv(reg, a, b):
    if type(b) == int:
        reg[a] = reg[a] // b
    else:
        reg[a] = reg[a] // reg[b]


def domod(reg, a, b):
    if type(b) == int:
        reg[a] = reg[a] % b
    else:
        reg[a] = reg[a] % reg[b]


def doequ(reg, a, b):
    if type(b) == int:
        reg[a] = 1 if reg[a] == b else 0
    else:
        reg[a] = 1 if reg[a] == reg[b] else 0


# Run loaded program
def runProgram(instr, vals):
    register = {"w": 0, "x": 0, "y": 0, "z": 0}

    for ins in instr:
        if ins[0] == 'inp':
            doinp(register, ins[1], vals.pop(0))
        elif ins[0] == "add":
            doadd(register, ins[1], ins[2])
        elif ins[0] == "mul":
            domul(register, ins[1], ins[2])
        elif ins[0] == "div":
            dodiv(register, ins[1], ins[2])
        elif ins[0] == "mod":
            domod(register, ins[1], ins[2])
        elif ins[0] == "equ":
            doequ(register, ins[1], ins[2])

    print(register)


def main():
    instr = parseInput(args.input)
    vals = [10]

    # Part 1
    runProgram(instr, vals)


if __name__ == "__main__":
    main()
