#!/usr/bin/python3

import argparse
import itertools
from copy import deepcopy

axis = ['x', 'y', 'z']

def main():
    # Check correct usage
    parser = argparse.ArgumentParser(description="Moon positional calculator.")
    parser.add_argument('pos', metavar='positions', type=str, help='Current moon positions.')
    args = parser.parse_args()

    # Parse memory
    try:
        moonpos = open(args.pos,'r')
    except IOError:
        sys.exit("Unable to open input file: " + args.pos)

    # Get moon positions
    moons = getMoons(moonpos)
    prev = [] # Just hold first value... if full loop. Once same value, all others will repeat, maybe wholly cyclic?

    # Calculate movement for n steps
    n = 100000
    for s in range(1,n+1):
    #s = 1
    #while True:
        applyGravity(moons)
        applyVelocity(moons)

        #print('After ' + str(s) + ' steps:')
        #for moon in moons:
        #    print('pos='+str(moon['x'][0])+','+str(moon['y'][0])+','+str(moon['z'][0])+'; '+'vel='+str(moon['x'][1])+','+str(moon['y'][1])+','+str(moon['z'][1]))

        energy = getEnergy(moons)
        if s == 1:
            prev = deepcopy(moons)
        elif moons == prev:
            print(s)
            break
        s += 1

def getMoons(startpos): # Parse moon starting positions in file.
    moons = []
    m = 0
    for line in startpos:
        moons.append({})

        line = line[1:-2] # strip newline and <>
        pos = line.split(', ')

        for i in range(0,3):
            # Axis: [pos,vel]
            moons[m][axis[i]] = [int(pos[i].split('=')[1]), 0]
        m += 1

    return moons

def applyGravity(moons):
    # Consider every pair (0,1) (0,2) (0,3) (1,2) (1,3) (2,3)
    for a, b in itertools.combinations(moons,2):
        for v in axis:
            if a[v][0] > b[v][0]:
                a[v][1] -= 1
                b[v][1] += 1
            elif a[v][0] < b[v][0]:
                a[v][1] += 1
                b[v][1] -= 1
    return

def applyVelocity(moons):
    for moon in moons:
        for v in axis:
            moon[v][0] += moon[v][1]

def getEnergy(moons):
    tot = 0
    for moon in moons:
        pot = abs(moon['x'][0]) + abs(moon['y'][0]) + abs(moon['z'][0])
        kin = abs(moon['x'][1]) + abs(moon['y'][1]) + abs(moon['z'][1])
        tot += pot * kin
    return tot

if __name__ == "__main__":
    main()
