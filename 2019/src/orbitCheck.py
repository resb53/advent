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

    #print(str(orbits))

    # Calculate orbit checksum
    chk = [0]
    
    for obj in orbits:
        chk[0] += 1
        #print(obj + ' orbits ' + orbits[obj] + '; chk=' + str(chk))
        countOrbits(orbits,orbits[obj],chk)
    
    print("Checksum: " + str(chk[0]))

    print("Hops to Santa: " + str(hopsBetween(orbits,'YOU','SAN')))

# Count how many orbits in system
def countOrbits(o,x,c):
    if x in o:
        #print(x + ' orbits ' + o[x] + '; c=' + str(c))
        c[0] += 1
        countOrbits(o,o[x],c)

# Count how many hops to get from a's orbit to share b's orbit
def hopsBetween(o,a,b):
    # Find each orbit
    orb = {}

    for x in [a, b]:
        orb[x] = findOrbit(o,x)

    # Find first common orbit (could there be more?)
    com = ''
    for common in orb[a]:
        if common in orb[b]:
            com = common
            break

    # Remove objects themselves
    orb[a].pop(0)
    orb[b].pop(0)

    # Calculate orbital hobs to join orbit
    hops = orb[a].index(com) + orb[b].index(com)
    return hops

# Return the orbit of an object or Nonetype if it orbits nothing
def findOrbit(o,x):
    orbit = []
    hub = ''
    while x in o:
        orbit.append(x)
        hub = o[x]
        x = o[x]
    orbit.append(hub)
    return orbit

if __name__ == "__main__":
    main()
