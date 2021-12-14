#!/usr/bin/env python3

import argparse
import sys
from collections import Counter

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

# Rather than recipe, give new pairings it produces
generate = {}
paircount = Counter()


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    pattern = input_fh.readline().strip("\n")
    _ = input_fh.readline()

    for line in input_fh:
        (pair, result) = line.strip("\n").split(" -> ")
        generate[pair] = (pair[0] + result, result + pair[1])

    for i in range(len(pattern) - 1):
        paircount[pattern[i] + pattern[i+1]] += 1


# For each pass, identify its seat
def stepThrough(polymer):
    '''startnode = polymer.head
    nextnode = startnode.next

    while nextnode is not None:
        newval = recipe[startnode.data][nextnode.data]
        counter[newval] += 1
        newnode = Node(newval)
        startnode.next = newnode
        newnode.next = nextnode

        startnode = nextnode
        nextnode = startnode.next'''


def main():
    parseInput(args.input)

    print(paircount)

    # Part 1
    '''for _ in range(10):
        stepThrough(poly)

    print(f"Solution to part 1: {max(counter.values()) - min(counter.values())}")'''

    # Part 2
    return


if __name__ == "__main__":
    main()
