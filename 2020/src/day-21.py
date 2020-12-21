#!/usr/bin/python3

import argparse
import sys
from collections import defaultdict

# Check correct usage
parser = argparse.ArgumentParser(description="Check your Passport.")
parser.add_argument('input', metavar='input', type=str,
                    help='Password list input.')
args = parser.parse_args()

ids = 0
foods = {}
allergens = {}
allpoint = defaultdict(list)
known = {}
candidates = defaultdict(list)


def main():
    parseInput(args.input)

    # Part 1
    print(findAllergenFree())

    # Part 2
    findKnown()
    sortedkeys = sorted(known.keys())
    print(",".join([known[i] for i in sortedkeys]))

    # Debug
    # printAllergens()


# Parse the input file
def parseInput(inp):
    global ids, foods, allergens
    try:
        menu_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in menu_fh:
        ings, alls = line.strip("\n").split(" (contains ")
        foods[ids] = ings.split(" ")
        allergens[ids] = alls[:-1].split(", ")
        for allergen in allergens[ids]:
            allpoint[allergen].append(ids)
        ids += 1


# Find list of ingredients without listed allergens
def findAllergenFree():
    global known, candidates

    for allergen in allpoint:
        # print(f"{allergen}:")
        candidates[allergen] = foods[allpoint[allergen][0]].copy()
        # print(candidates[allergen])

        # Remove known allergen
        for bye in known.values():
            if bye in candidates[allergen]:
                candidates[allergen].remove(bye)

        # Remove impossible allergens
        if len(allpoint[allergen]) > 1:
            for id in allpoint[allergen][1:]:
                remove = []
                for ing in candidates[allergen]:
                    if ing not in foods[id]:
                        remove.append(ing)
                for bye in remove:
                    candidates[allergen].remove(bye)

                # print(candidates[allergen])

        # Update known allergens
        if len(candidates[allergen]) == 1:
            known[allergen] = candidates[allergen][0]

    for allergen in candidates:
        print(f"{allergen}: {candidates[allergen]}")

    print(known)

    candlist = []
    for alllist in candidates.values():
        for allergic in alllist:
            if allergic not in candlist:
                candlist.append(allergic)

    appearances = 0
    for id in foods:
        for ing in foods[id]:
            if ing not in candlist:
                appearances += 1

    return appearances


def findKnown():
    while len(candidates) > 0:
        remkey = []

        for allergen in candidates:
            remove = []

            for ing in candidates[allergen]:
                if ing in known.values():
                    remove.append(ing)

            for bye in remove:
                candidates[allergen].remove(bye)

            if len(candidates[allergen]) == 1:
                known[allergen] = candidates[allergen][0]

            elif len(candidates[allergen]) == 0:
                remkey.append(allergen)

        while len(remkey) > 0:
            candidates.pop(remkey.pop(0))


def printAllergens():
    for i in allergens:
        print(allergens[i])


if __name__ == "__main__":
    main()
