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

    wires = [] # List of wires {x: {y: 1}} for all locations crossed by wire,
    w = 0 # wire number

    # Parse instructions in file. Allow for multiline just in case future need.
    for line in instr_fh:
        cmd = line.rsplit()[0]
        wires.append({})
        pos = [0, 0] # [x, y]
        d = 0 # distance travelled to this point

        # Split command string into list of instructions
        instr = cmd.split(',')
        move = []

        # Parse movements
        for x in instr:
            a = x[0]
            b = x[1:]
            move.append([a, int(b)])

        for mvmt in move:
            j = calculatePos(pos, mvmt)
            for i in j:
                # 1 more distance travelled
                d += 1
                #create new y dict if x not seen before
                if i[0] not in wires[w]:
                    wires[w][i[0]] = {}
                # if not travelled here before
                if i[1] not in wires[w][i[0]]:
                    wires[w][i[0]][i[1]] = d
                #print(str(wires[w]))
            pos = [i[0],i[1]]

        w += 1

    cross = findCrossings(wires)
    print(str(cross))

    minman = manhattan(cross.pop(0))
    print("minman: " + str(minman))
    for locn in cross:
        manh = manhattan(locn)
        if manh < minman:
            minman = manh
    print("Min Manhattan: " + str(minman))

def calculatePos(start, repos):
    journey = []
    #print("Start: " + str(start) + "; Repos: " + str(repos))
    if (repos[0] == 'R'):
        end = start[0] + repos[1]
        while (start[0] != end):
            start[0] += 1
            journey.append([start[0],start[1]])
    elif (repos[0] == 'U'):
        end = start[1] + repos[1]
        while (start[1] != end):
            start[1] += 1
            journey.append([start[0],start[1]])
    elif (repos[0] == 'L'):
        end = start[0] - repos[1]
        while (start[0] != end):
            start[0] -= 1
            journey.append([start[0],start[1]])
    elif (repos[0] == 'D'):
        end = start[1] - repos[1]
        while (start[1] != end):
            start[1] -= 1
            journey.append([start[0],start[1]])
    else:
        sys.exit("Unable to parse direction parameter: " + str(repos[0]))
    return journey

def findCrossings(wirelist): # ASSUMES ONLY 2 WIRES AT THE MOMENT
    crossings = [];
    for x in wirelist[0]:
        for y in wirelist[0][x]:
            if x in wirelist[1]:
                if y in wirelist[1][x]:
                    crossings.append([x,y])
    return crossings

def manhattan(coords): # Calculate Manhattan distance of coordinate from origin
    [x,y] = coords
    if (x < 0):
        x *= -1
    if (y < 1):
        y *= -1
    return x + y

main()
