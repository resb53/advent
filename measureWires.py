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

    wires = [] # List of list of positions for each wire [x, y],
    w = 0 # wire number

    # Parse instructions in file. Allow for multiline just in case future need.
    for line in instr_fh:
        cmd = line.rsplit()[0]
        wires.append([])
        pos = [0, 0] # [x, y]
        move = []

        # Split command string into list of instructions
        instr = cmd.split(',')

        # Parse movements
        for x in instr:
            a = x[0]
            b = x[1:]
            move.append([a, int(b)])

        for mvmt in move:
            calculatePos(pos, mvmt)
            wires[w].append([pos[0],pos[1]])

        w += 1

    cross = findCrossings(wires)
    print(str(cross))

def calculatePos(start, repos):
    if (repos[0] == 'R'):
        start[0] += repos[1]
    elif (repos[0] == 'U'):
        start[1] += repos[1]
    elif (repos[0] == 'L'):
        start[0] -= repos[1]
    elif (repos[0] == 'D'):
        start[1] -= repos[1]
    else:
        sys.exit("Unable to parse direction parameter: " + str(repos[0]))
    return start

def findCrossings(wirelist): # ASSUMES ONLY 2 WIRES AT THE MOMENT
    crossings = [];
    for a in wirelist[0]:
        for b in wirelist[1]:
            if ( (a[0] == b[0]) and (a[1] == b[1]) ):
                crossings.append([a[0],a[1]])
    return crossings

main()
