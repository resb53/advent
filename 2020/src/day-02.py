#!/usr/bin/python3

import argparse
import sys
from copy import deepcopy

# Check correct usage
parser = argparse.ArgumentParser(description="Check your passwords.")
parser.add_argument('input', metavar='input', type=str, help='Password list input.')
args = parser.parse_args()

passwords = []


def main():
    parseInput(args.input)
    findValid()
    findActual()


# Parse the input file
def parseInput(inp):
    global passwords
    try:
        pws_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in pws_fh:
        line = line.strip("\n")
        # Split into critical parts
        pword = line.split()
        (mini, maxi) = pword[0].split('-')
        pword.insert(0,int(mini))
        pword[1] = int(maxi)
        pword[2] = pword[2].strip(":")

        passwords.append(pword)


# Calculate the rows with errors
def findValid():
    valid = 0

    for pword in passwords:
        #print(str(pword))
        count = pword[3].count(pword[2])

        if pword[0] <= count and count <= pword[1]:
            valid = valid + 1

    print(valid)


# Part 2 - find true passwords
def findActual():
    actual = 0

    for pword in passwords:
        # Conditions met
        met = 0

        if pword[3][pword[0]-1] == pword[2]:
            met = met + 1

        if pword[3][pword[1]-1] == pword[2]:
            met = met + 1

        if met == 1:
            actual = actual + 1

    print(actual)


if __name__ == "__main__":
    main()
