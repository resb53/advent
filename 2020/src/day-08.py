#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Code.")
parser.add_argument('input', metavar='input', type=str,
                    help='Code input.')
args = parser.parse_args()

code = []
acc = 0
exo = []  # Execution Order


def main():
    parseInput(args.input)

    # Part 1
    executeCode()

    # Part 2

    # Debug
    # printCode()


# Parse the input file
def parseInput(inp):
    global code
    try:
        code_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in code_fh:
        op, arg = line.strip("\n").split(" ")
        code.append([op, int(arg)])


# For each pass, identify its seat
def executeCode():
    global acc
    step = 0

    while step not in exo:
        exo.append(step)
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


def printCode():
    for item in code:
        print(item)


if __name__ == "__main__":
    main()
