#!/usr/bin/python3

import sys

# Check correct usage
if (len(sys.argv) != 2):
    sys.exit("USAGE: " + sys.argv[0] + " inputs_filename")

# Parse memory
try:
    instr_fh = open(sys.argv[1],'r')
except IOError:
    sys.exit("Unable to open input file: " + sys.argv[1])

def main():
    # Build dict for every item you see that points to what it orbits
    orbits = {}

    # Parse instructions in file. Allow for multiline just in case future need.
    for line in instr_fh:
        line = line.rsplit()[0]
        rel = line.split(')')

        orbits[rel[1]] = rel[0]

    print(str(orbits))

    # Calculate orbit checksum
    chk = 0

    for obj in orbits:
        print(obj + ' orbits ' + orbits[obj] + '; chk=' + str(chk))
        chk += 1
        countOrbits(orbits,orbits[obj],chk)

    print(chk)        

def countOrbits(o,x,c):
    if x in o:
        print(x + ' orbits ' + o[x] + '; c=' + str(c))
        c += 1
        countOrbits(o,o[x],c)

if __name__ == "__main__":
    main()
