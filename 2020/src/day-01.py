#!/usr/bin/python3

import argparse
import sys
from copy import deepcopy

# Check correct usage
parser = argparse.ArgumentParser(description="Check your accounts.")
parser.add_argument('input', metavar='input', type=str, help='Account input.')
args = parser.parse_args()

accounts = []


def main():
    global accounts
    parseInput(args.input)
    findErrors()


def parseInput(inp):
    global accounts
    try:
        accounts_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in accounts_fh:
        line = line.strip("\n")
        accounts.append(int(line))

    accounts = sorted(accounts)


def findErrors():
    for entry in accounts:
        print(entry)


if __name__ == "__main__":
    main()
