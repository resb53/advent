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


def doeql(reg, a, b):
    if type(b) == int:
        reg[a] = 1 if reg[a] == b else 0
    else:
        reg[a] = 1 if reg[a] == reg[b] else 0


# Run loaded program
def runProgram(instr, vals):
    vals = vals.copy()
    register = {"w": 0, "x": 0, "y": 0, "z": 0}

    for i, ins in enumerate(instr):
        print(f"{i}: {register}")
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
        elif ins[0] == "eql":
            doeql(register, ins[1], ins[2])
        if i % 18 == 0:
            print(register["z"])

    return register["z"]


# Analyse Ops
def analyseOps(instr):
    analyse = instr.copy()
    # Manual observation, blocks of 18 similar instructions. Check this:
    n = 1
    while len(analyse) > 0:
        block, analyse = analyse[0:18], analyse[18:]
        print(f"Block {n}:")
        # Read next value into W
        if block[0] != ["inp", "w"]:
            print(f"{n}, 0: {block[0]}")
        # Set X = 0
        if block[1] != ["mul", "x", 0]:
            print(f"{n}, 1: {block[1]}")
        # Set X = prevZ
        if block[2] != ["add", "x", "z"]:
            print(f"{n}, 2: {block[2]}")
        # X = prevZ mod 26
        if block[3] != ["mod", "x", 26]:
            print(f"{n}, 3: {block[3]}")
        # Z = prevZ OR prevZ // 26
        if block[4][0:2] != ["div", "z"]:
            print(f"{n}, 4: {block[4]}")
        else:
            print(f"4: {block[4][2]}", end="")
        # X = (Z mod 26 + A)
        if block[5][0:2] != ["add", "x"]:
            print(f"{n}, 5: {block[5]}")
        else:
            print(f", 5: {block[5][2]}", end="")
        # X = 1 if (Z mod 26 + A) == W else 0
        if block[6] != ["eql", "x", "w"]:
            print(f"{n}, 6: {block[6]}")
        # X = 1 if (Z mod 26 + A) != W else 0
        if block[7] != ["eql", "x", 0]:
            print(f"{n}, 7: {block[7]}")
        # Y = 0
        if block[8] != ["mul", "y", 0]:
            print(f"{n}, 8: {block[8]}")
        # Y = 25
        if block[9] != ["add", "y", 25]:
            print(f"{n}, 9: {block[9]}")
        # Y = 25 if (Z mod 26 + A) != W else 0
        if block[10] != ["mul", "y", "x"]:
            print(f"{n}, 10: {block[10]}")
        # Y = 26 if (Z mod 26 + A) != W else 1
        if block[11] != ["add", "y", 1]:
            print(f"{n}, 11: {block[11]}")
        # Z = (26 * Z) if (Z mod 26 + A) != W else Z
        if block[12] != ["mul", "z", "y"]:
            print(f"{n}, 12: {block[12]}")
        # Y = 0
        if block[13] != ["mul", "y", 0]:
            print(f"{n}, 13: {block[13]}")
        # Y = W
        if block[14] != ["add", "y", "w"]:
            print(f"{n}, 14: {block[14]}")
        # Y = W + B
        if block[15][0:2] != ["add", "y"]:
            print(f"{n}, 15: {block[15]}")
        else:
            print(f", 15: {block[15][2]}")
        # Y = (W + B) if (Z mod 26 + A) != W else 0
        if block[16] != ["mul", "y", "x"]:
            print(f"{n}, 16: {block[16]}")
        # Z = ((26 * Z) + (W + B)) if (Z mod 26 + A) != W else Z
        if block[17] != ["add", "z", "y"]:
            print(f"{n}, 17: {block[17]}")
        n += 1


def simplifyInput(instr):
    analyse = instr.copy()
    simplified = []
    while len(analyse) > 0:
        block, analyse = analyse[0:18], analyse[18:]
        simplified.append([block[4][2], block[5][2], block[15][2]])

    return simplified


def runSimply(instr, input):
    input = input.copy()
    register = {"w": 0, "x": 0, "y": 0, "z": 0}

    for vars in instr:
        print(register["z"])
        register["w"] = input.pop(0)
        register["z"] = register["z"] // vars[0]
        if (register["z"] % 26) + vars[1] != register["w"]:
            register["z"] = ((26 * register["z"]) + register["w"] + vars[2])

    return register["z"]


def main():
    instr = parseInput(args.input)
    simpl = simplifyInput(instr)

    # Part 1
    input = [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 1,
        2, 3, 4, 5
    ]

    # analyseOps(instr)
    print(runProgram(instr, input))
    print(runSimply(simpl, input))


if __name__ == "__main__":
    main()
