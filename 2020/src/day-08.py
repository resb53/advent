#!/usr/bin/python3

import argparse
import sys
from handheld import Handheld

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Code.")
parser.add_argument('input', metavar='input', type=str,
                    help='Code input.')
args = parser.parse_args()

incode = []


def main():
    parseInput(args.input)

    # Part 1
    cpu = Handheld(incode)
    cpu.execute()

    # Part 2
    findBug(cpu)

    # Debug
    # printCode()


# Parse the input file
def parseInput(inp):
    global incode
    try:
        code_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in code_fh:
        op, arg = line.strip("\n").split(" ")
        incode.append([op, int(arg)])


# Find bug
def findBug(cpu):
    # list all potention ops to change
    for step in range(len(incode)):
        test = False

        if incode[step][0] == 'jmp':
            reset = 'jmp'
            incode[step][0] = 'nop'
            test = True
        elif incode[step][0] == 'nop':
            reset = 'nop'
            incode[step][0] = 'jmp'
            test = True

        if test:
            cpu.load(incode)
            if cpu.execute() == 0:
                print(f"Ended gracefully, acc: {cpu.acc}")
                return 0  # Bug found

            else:
                incode[step][0] = reset

    return 1  # Bug not found


def printCode():
    for item in incode:
        print(f"End: {item}")


if __name__ == "__main__":
    main()
