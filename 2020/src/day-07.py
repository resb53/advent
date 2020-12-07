#!/usr/bin/python3

import argparse
import sys
import re

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Bags.")
parser.add_argument('input', metavar='input', type=str,
                    help='Bag rule list input.')
args = parser.parse_args()

rules = {}
holdsgold = []


def main():
    global holdsgold
    parseInput(args.input)

    # Part 1
    # Check for directly holding
    holdsgold = findBags("shiny gold")

    # Check for indirectly holding
    new = holdsgold.copy()
    redo = True

    while redo:
        newnew = []
        print(f"Checking... {new}")

        for item in new:
            check = findBags(item)

            for test in check:
                if test not in holdsgold:
                    newnew.append(test)
                    holdsgold.append(test)

        if len(newnew) == 0:
            redo = False

        else:
            new = newnew

    print(f"Total in holdsgold: {len(holdsgold)}.")

    # Part 2
    contained = countBags("shiny gold")
    count = len(contained)

    while len(contained) > 0:
        print(f"Contained: {contained}, count: {count}")
        add = contained.pop(0)
        print(f"Check: {add}...")
        new = countBags(add)
        count += len(new)
        contained.extend(new)

    print(f"Total bags to buy: {count}")

    # Debug
    # printRules()


# Parse the input file
def parseInput(inp):
    global passes
    try:
        rules_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in rules_fh:
        line = line.strip("\n")
        match = re.match(r"^(\w+ \w+) bags contain (.+)\.$", line, re.I)
        if not match:
            print(f"Error: Can't parse line: {line}")
        else:
            container = match.group(1)
            contents = match.group(2)
            # print(f"Container: {container}, Content: {content}")

        # Parse the contents
        if contents == "no other bags":
            match = []
        else:
            match = re.findall(r"\d+ (\w+ \w+) bag", contents, re.I)
            if not match:
                print(f"Error: Can't parse contents: {contents}")

        if container in rules:
            print(f"Already seen '{container}'.")
        else:
            rules[container] = match


# For specified bag, how many can contain it?
def findBags(bagtype):
    holds = []

    for item in rules:
        if bagtype in rules[item]:
            holds.append(item)

    return(holds)


def printRules():
    for item in rules:
        print(f"{item}: {rules[item]}")


def countBags(bagtype):
    contains = rules[bagtype]

    return contains


if __name__ == "__main__":
    main()
