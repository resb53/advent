#!/usr/bin/python3

import argparse
import itertools
from copy import deepcopy
from math import gcd

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
    prev = deepcopy(moons) # Just hold first value... if full loop. Once same value, all others will repeat, maybe wholly cyclic?
    period = [0,0,0]

    # Calculate movement for n steps
    #n = 100000 # 2.5 secs for 100k implies 32.5 hours for test2's 4.6Bn
    #for s in range(1,n+1):
    s = 1
    while period[0] == 0 or period[1] == 0 or period[2] == 0:
        applyGravity(moons)
        applyVelocity(moons)
        energy = getEnergy(moons)
        # Compare each dimension
        if period[0] == 0:
            if getDim('x',moons) == getDim('x',prev):
                period[0] = s
        if period[1] == 0:
            if getDim('y',moons) == getDim('y',prev):
                period[1] = s
        if period[2] == 0:
            if getDim('z',moons) == getDim('z',prev):
                period[2] = s
        s += 1

    # Calculate LCM of periods
    lcm = int(period[0] * period[1] / (gcd(period[0], period[1])))
    lcm = int(lcm * period[2] / (gcd(lcm, period[2])))

    print(lcm)


def getDim(v,moons):
    dim = []
    for i in moons:
        dim.append(i[v])
    return dim


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
