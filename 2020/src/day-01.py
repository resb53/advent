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


# Parse the input file
def parseInput(inp):
    global accounts, backward
    try:
        accounts_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in accounts_fh:
        line = line.strip("\n")
        accounts.append(int(line))

    accounts = sorted(accounts)


# Calculate the rows with errors
def findErrors():
    size = len(accounts)

    for i in range(size):
        #print(accounts[i])
        add = 5000
        check = size - 1

        while add > 2020:
            add = accounts[i] + accounts[check]
            #print (str(accounts[i]) + ' + ' + str(accounts[check]) + ' = ' + str(add))
            check = check - 1

        #print(str(add) + ' = ' + str(accounts[i]) + ' + ' + str(accounts[check + 1]))
        if add == 2020:
            print('2020 = ' + str(accounts[i]) + ' + ' + str(accounts[check + 1]))
            print('Answer is: ' + str(accounts[i] * accounts[check + 1]))
            break


if __name__ == "__main__":
    main()
