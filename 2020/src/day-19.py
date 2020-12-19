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
    print(findMatches())

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
                        # print(f"In {rules[key]}:\n{opt} can be solved.")
                        # Update
                        if len(opt) > 1:
                            update = mergeKeys(opt)
                        else:
                            # if this opt not already solved
                            if isinstance(opt[0], int):
                                update = rules[opt[0]]
                            else:
                                update = opt
                        rules[key][i] = update
                        # print(f"Result: {rules[key]}\n")
                    else:
                        solve = False

                if solve:
                    # print(f"Solving {rules[key]}:")
                    opts = []
                    for chunk in rules[key]:
                        for opt in chunk:
                            opts.append(opt)
                    rules[key] = opts
                    # print(f"Result: {rules[key]}\n")
                    solved.append(key)

        # printRules()
        # print("")

    # print(rules[0])

    count = 0
    for img in images:
        if img in rules[0]:
            count += 1
    return count


def mergeKeys(keylist):
    ret = ['']
    # Work through tuples
    for append in keylist:
        update = []
        if isinstance(append, int):
            conjoin = rules[append]
        else:
            conjoin = [append]
        # print(f"Merging {ret} with {conjoin}...")
        for first in ret:
            for last in conjoin:
                update.append(first + last)
        ret = update

    return ret


def printRules():
    for num in rules:
        print(f"{num}: {rules[num]}")


if __name__ == "__main__":
    main()
