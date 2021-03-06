#!/usr/bin/python3

import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Watch oxygen fill the room.")
parser.add_argument('inp', metavar='inp', type=str, help='Input array.')
parser.add_argument('-p', metavar='phases', type=int, default=1, help='Number of phases to iterate (def=1).')
args = parser.parse_args()

signal = [] # Signal array
mod = [] # Modulations
seed = [0, 1, 0, -1] # Mod seeds

# Part 2 thoughts: for elements n to n+7, only columns and rows between n and end matter
# Far fewer calculations to start at the right element, and only do 8 rows for it
# But how to quickly get the right seed for these elements?

def main():
    global signal, mod
    signal = getInput(args.inp)

    # First just see how long it takes to get digits from n to end <- returns in 0.271s
    skip = ''
    for i in range(0, 7):
        skip += str(signal[i])
    print('Skip:' + skip)
    signal = 10000 * signal
    signal = signal[int(skip):] # curbed
    print('Curb:' + str(len(signal)))
    # Calculate len(curbed) mod arrays for signal from n to end
    #mod = prepMods(len(signal), int(skip)) # <- returns 30 rows in 1m30, 526569 rows in 
    for rep in range(0, args.p):
        signal = processSignal(signal, mod)

def getInput(inp):
    try:
        grid_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    arr = list(str(grid_fh.readline().strip('\n')))
    arr = [ int(x) for x in arr ]

    return arr

def prepMods(l, skip):
    mods = []
    # Rows
    for i in range(skip+1, l+1):
        # Columns
        col = []
        j = 0
        while len(col) < l+1:
            col.extend(seedGen(i, j))
            j += 1
        mods.append(col[skip+1:l+1])
        print(len(mods[0]))
    return mods

def seedGen(i, j):
    gen = []
    for p in range(0, i):
       gen.append(seed[j % 4])
    return gen 

def processSignal(sig, mod):
    output = []
    l = len(sig)
    # Rows
    total = sum(sig)
    output.append(int(str(total)[-1]))
    for i in range(1, l):
        total -= sig[i-1]
        output.append(int(str(total)[-1]))
    print(output[0:8])
    return output

if __name__ == "__main__":
    main()
