#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Code.")
parser.add_argument('input', metavar='input', type=str,
                    help='Code input.')
args = parser.parse_args()

incode = []
acc = 0
exo = []  # Execution Order


def main():
    parseInput(args.input)

    # Part 1
    executeCode(incode)

    # Part 2
    findBug()

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


# For each pass, identify its seat
def executeCode(code):
    global acc, exo
    acc = 0
    step = 0
    exo = []

    while step not in exo:
        exo.append(step)
        # Exit gracefully
        if step < 0 or step >= len(code):
            return 0

        op = code[step][0]
        arg = code[step][1]

        # Execute step
        if op == 'acc':
            acc += arg
            step += 1

        elif op == 'jmp':
            step = step + arg

        elif op == 'nop':
            step += 1

        else:
            sys.exit(f"Unknown argument on line {step}: {arg}")

    print(acc)
    return 1


# Find bug
def findBug():
    # list all potention ops to change
    for step in range(len(incode)):
        test = False
        testcode = incode.copy()

        if testcode[step][0] == 'jmp':
            testcode[step][0] == 'nop'
            test = True
        elif testcode[step][0] == 'nop':
            testcode[step][0] == 'jmp'
            test = True

        if test:
            print(f"Test line: {step}")

            if executeCode(testcode) == 0:
                print(acc)
                return 0  # Bug found

    return 1  # Bug not found


def printCode():
    for item in code:
        print(f"End: {item}")


if __name__ == "__main__":
    main()
