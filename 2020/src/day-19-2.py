#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your image messages.")
parser.add_argument('input', metavar='input', type=str,
                    help='Message rule input.')
args = parser.parse_args()

rules = {}
messages = []
solved = []


def main():
    parseInput(args.input)

    # Part 1
    evalRules()

    # Part 2

    # Debug
    printRules()


# Parse the input file
def parseInput(inp):
    global rules, messages, solved
    try:
        rules_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    msgs = False

    for line in rules_fh:
        line = line.strip("\n")

        if len(line) == 0:
            msgs = True

        if not msgs:
            key, rule = line.split(": ")
            key = int(key)
            rules[key] = []
            for opt in rule.split(" | "):
                if "\"" in opt:
                    rules[key] = [opt[1]]
                    solved.append(key)
                else:
                    rules[key].append([int(i) for i in opt.split(" ")])

        else:
            messages.append(line)


# For each pass, identify its seat
def evalRules():
    global rules, solved

    for key in rules:
        if key not in solved:
            update = []

            for i, opt in enumerate(rules[key]):
                solve = True
                for bit in opt:
                    if bit not in solved:
                        solve = False

                if solve:
                    update.append(i)

            if len(update) > 0:
                    rules[key] = updateRule(rules[key], update)


# For the sections with all parts solved, update the rule
def updateRule(rule, sections):
    update = []

    for i, opt in enumerate(rule):
        if i in sections:
            newopts = []

            # Work through tuples, combining

            update.extend(newopts)

        else:
            update.append(opt)

    return update


def printRules():
    for key in rules:
        print(f"{key}: {rules[key]}")


if __name__ == "__main__":
    main()
