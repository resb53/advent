#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Images.")
parser.add_argument('input', metavar='input', type=str,
                    help='Image list input.')
args = parser.parse_args()

rules = {}
images = []
solved = []


def main():
    parseInput(args.input)

    # Part 1
    findMatches()

    # Part 2

    # Debug
    # printRules()


# Parse the input file
def parseInput(inp):
    global rules, images, seeds
    try:
        rules_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    img = False
    for line in rules_fh:
        line = line.strip("\n")
        if line == "":
            img = True
        elif img:
            images.append(line)
        else:
            key, val = line.split(": ")
            rules[int(key)] = []
            vals = val.split(" | ")
            for opt in vals:
                if "\"" in opt:
                    rule = opt[1]
                    solved.append(int(key))
                else:
                    rule = [int(i) for i in opt.split(" ")]
                rules[int(key)].append(rule)


# For each pass, identify its seat
def findMatches():
    global rules
    # Iterate through rules updating options for any known rules
    while 0 not in solved:
        for key in rules:
            if key not in solved:
                solve = True

                for i, opt in enumerate(rules[key]):
                    done = True

                    for check in opt:
                        if isinstance(check, int):
                            if check not in solved:
                                done = False

                    if done:
                        # print(f"{key} part {i} is done.")
                        # Update
                        if len(opt) > 1:
                            update = mergeKeys(opt)
                        else:
                            update = rules[opt[0]]
                        rules[key][i] = update
                    else:
                        solve = False

                if solve:
                    opts = []
                    for chunk in rules[key]:
                        for opt in chunk:
                            opts.append(opt)
                    rules[key] = opts
                    solved.append(key)

        # solved.append(0)
        printRules()
        print("")


def mergeKeys(keylist):
    ret = []
    # Always tuples?
    for first in rules[keylist[0]]:
        for last in rules[keylist[1]]:
            ret.append(first + last)
    return ret


def printRules():
    for num in rules:
        print(f"{num}: {rules[num]}")


if __name__ == "__main__":
    main()
