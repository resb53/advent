#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Watch oxygen fill the room.")
parser.add_argument('inp', metavar='inp', type=str, help='Input array.')
args = parser.parse_args()

signal = [] # Signal array
mod = [] # Modulations
seed = [0, 1, 0, -1] # Mod seeds

def main():
    global signal, mod
    signal = getInput(args.inp)
    mod = prepMods(len(signal))
    print(mod)
    signal = processSignal(signal, mod)

def getInput(inp):
    try:
        grid_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    line = grid_fh.readline().strip('\n')

    return list(str(line))

def prepMods(l):
    mods = []
    # Rows
    for i in range(1, l+1):
        # Columns
        col = []
        j = 0
        while len(col) < l+1:
            col.extend(seedGen(i, j))
            j += 1
        mods.append(col[1:l+1])

    return mods

def seedGen(i, j):
    gen = []
    for p in range(0, i):
       gen.append(seed[j % 4])
    return gen 

def processSignal(sig, mod):
    return

if __name__ == "__main__":
    main()
