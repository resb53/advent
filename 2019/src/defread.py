#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Watch oxygen fill the room.")
parser.add_argument('inp', metavar='inp', type=str, help='Input array.')
args = parser.parse_args()

signal = [] # Signal array

def main():
    global signal
    signal = getInput(args.inp)
    print(signal)

def getInput(inp):
    try:
        grid_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    line = grid_fh.readline().strip('\n')

    return line

if __name__ == "__main__":
    main()
