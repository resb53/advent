#!/usr/bin/python3

import argparse
import sys
from copy import deepcopy

# Check correct usage
parser = argparse.ArgumentParser(description="Navigate the maze.")
parser.add_argument('map', metavar='map', type=str, help='Map input.')
args = parser.parse_args()

grid = {} # map[y][x] symbols
floor = []
portals = {} # x,y to x,y
pos = [0,0] # x, y
minx, miny, maxx, maxy = 0, 0, 0, 0

def main():
    global grid, portals, pos
    parseInput(args.map)
    # Part 2: Shortest route AA to ZZ across floors
    getPortals()
    # Prep floors
    prepFloors()
    # Calculate path
    print(calcRoutes())

def parseInput(inp):
    global grid, pos
    try:
        grid_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    y = 0
    x = 0

    for line in grid_fh:
        line = line.strip("\n")
        grid[y] = {}
        for ch in list(line):
            grid[y][x] = ch
            x += 1
        y += 1
        x = 0

def printGrid(g):
    for y in g:
        for x in g[y]:
            if len(g[y][x]) > 1:
                print('@', end='')
            else:
                print(g[y][x], end='')
        print('')

def prepFloors():
    global floor, grid
    # Ground (0) and -1 (1) floor
    floor.append(deepcopy(grid))
    floor.append(deepcopy(grid))
    # Block upstairs and remove exits downstairs
    for y in grid:
        for x in grid[y]:
            if len(grid[y][x]) > 1:
                if x < minx or x > maxx or y < miny or y > maxy:
                    floor[0][y][x] = '#'
            elif grid[y][x] == '$' or grid[y][x] == '£':
                floor[1][y][x] = '#'
    # Update grid for future floors
    grid = deepcopy(floor[1])

def getPortals():
    global grid, portals, pos, minx, miny, maxx, maxy
    # Get corner coords
    for y in grid:
        for x in grid[y]:
            if grid[y][x] == '#':
                if minx == 0 and miny == 0:
                    minx, miny = x, y
                maxx, maxy = x, y

    for y in grid:
        for x in grid[y]:
            ch = grid[y][x]
            check = [[y-1, x, y-2, x, '-'], [y+1, x, y+2, x, '+'], [y, x+1, y, x+2, '+'], [y, x-1, y, x-2, '-']]
            if ch == '.':
                # Check neighbours to find portal
                portal = 0
                for v in check:
                    if grid[v[0]][v[1]].isupper() and len(grid[v[0]][v[1]]) == 1:
                        if v[4] == '+':
                            fc = grid[v[0]][v[1]]
                            sc = grid[v[2]][v[3]]
                        else:
                            fc = grid[v[2]][v[3]]
                            sc = grid[v[0]][v[1]]
                        p = fc + sc
                        if p == 'AA':
                            pos = [x, y]
                            grid[y][x] = '$'
                        elif p == 'ZZ':
                            grid[y][x] = '£'
                        else:
                            if p not in portals:
                                portals[p] = []
                            # Choose +1 or -1 based on bounds of map
                            if v[1] < minx or v[1] > maxx or v[0] < miny or v[0] > maxy:
                                portals[p].append([v[1], v[0], 1])
                            else:
                                portals[p].append([v[1], v[0], -1])
                            grid[v[0]][v[1]] = p
                            grid[v[2]][v[3]] = ' '

def calcRoutes():
    global floor
    count = 0
    floor[0][pos[1]][pos[0]] = '█'
    done = False

    while done == False:
    #while count < 30:
        count += 1
        floor, done = expand(floor)

        if count % 50 == 0:
            print("Step:" + str(count) + " Depth:" + str(len(floor)))
        #for g in floor:
        #    printGrid(g)

    return(count)

def expand(f):
    depth = 0
    expanded = []
    done = False
    for g in f:
        for y in g:
            for x in g[y]:
                check = [[y-1, x], [y+1, x], [y, x+1], [y, x-1]]
                if g[y][x] == '█':
                    # Expand
                    for v in check:
                        if g[v[0]][v[1]] == '.':
                            expanded.append([v[0], v[1], '.', depth])
                        elif len(g[v[0]][v[1]]) > 1:
                            p = g[v[0]][v[1]]
                            if [portals[p][0][0], portals[p][0][1]] == [v[1], v[0]]:
                                expanded.append([portals[p][1][1], portals[p][1][0], 'p', depth + portals[p][1][2]])
                                g[portals[p][0][1]][portals[p][0][0]] = '█'
                            else:
                                expanded.append([portals[p][0][1], portals[p][0][0], 'p', depth + portals[p][0][2]])
                                g[portals[p][1][1]][portals[p][1][0]] = '█'
                        elif g[v[0]][v[1]] == '£':
                            done = True
        depth += 1

    if len(expanded) > 0:
        for p in expanded:
            if p[2] == '.':
                f[p[3]][p[0]][p[1]] = '█'
            else:
                expandTile(p[1], p[0], p[3])
        return [f, done]
    else:
        return [f, True]

def expandTile(x, y, d):
    global floor
    if d >= len(floor):
        floor.append(deepcopy(grid))
    g = floor[d]
    for v in [[y-1, x], [y+1, x], [y, x+1], [y, x-1]]:
        if g[v[0]][v[1]] == '.':
            g[v[0]][v[1]] = '█'
    g[y][x] = '█'

if __name__ == "__main__":
    main()
