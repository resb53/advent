#!/usr/bin/python3

import argparse
import sys
from copy import deepcopy

# Check correct usage
parser = argparse.ArgumentParser(description="Navigate the maze.")
parser.add_argument('map', metavar='map', type=str, help='Map input.')
args = parser.parse_args()

grid = {} # map[y][x] symbols
portals = {} # x,y to x,y
pos = [0,0] # x, y

def main():
    global grid, portals, pos
    parseInput(args.map)
    # Part 1: Shortest route AA to ZZ
    getPortals()
    print(portals)
    # Set start
    calcRoutes()

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

def getPortals():
    global grid, portals, pos
    for y in grid:
        for x in grid[y]:
            ch = grid[y][x]
            if ch == '.':
                # Check neighbours to find portal
                portal = 0
                if grid[y-1][x].isupper() and len(grid[y-1][x]) == 1:
                    fc = grid[y-2][x]
                    sc = grid[y-1][x]
                    p = fc + sc
                    if p == 'AA':
                        pos = [x, y]
                        grid[y][x] = '$'
                    elif p == 'ZZ':
                        grid[y][x] = '£'
                    else:
                        if p not in portals:
                            portals[p] = []
                        portals[p].append([x, y-1])
                        grid[y-1][x] = p
                        grid[y-2][x] = ' '
                if grid[y+1][x].isupper() and len(grid[y+1][x]) == 1:
                    fc = grid[y+1][x]
                    sc = grid[y+2][x]
                    p = fc + sc
                    if p == 'AA':
                        pos = [x, y]
                        grid[y][x] = '$'
                    elif p == 'ZZ':
                        grid[y][x] = '£'
                    else:
                        if p not in portals:
                            portals[p] = []
                        portals[p].append([x, y+1])
                        grid[y+1][x] = p
                        grid[y+2][x] = ' '
                if grid[y][x+1].isupper() and len(grid[y][x+1]) == 1:
                    fc = grid[y][x+1]
                    sc = grid[y][x+2]
                    p = fc + sc
                    if p == 'AA':
                        pos = [x, y]
                        grid[y][x] = '$'
                    elif p == 'ZZ':
                        grid[y][x] = '£'
                    else:
                        if p not in portals:
                            portals[p] = []
                        portals[p].append([x+1, y])
                        grid[y][x+1] = p
                        grid[y][x+2] = ' '
                if grid[y][x-1].isupper() and len(grid[y][x-1]) == 1:
                    fc = grid[y][x-2]
                    sc = grid[y][x-1]
                    p = fc + sc
                    if p == 'AA':
                        pos = [x, y]
                        grid[y][x] = '$'
                    elif p == 'ZZ':
                        grid[y][x] = '£'
                    else:
                        if p not in portals:
                            portals[p] = []
                        portals[p].append([x-1, y])
                        grid[y][x-1] = p
                        grid[y][x-2] = ' '

def calcRoutes():
    global grid
    count = 0
    grid[pos[1]][pos[0]] = ','
    done = False

    #while done == False:
    while count <= 5:
        count += 1
        print(count)
        grid, done = expand(grid)
        printGrid(grid)

def expand(g):
    # No bound checking as surrounding wall
    expanded = []
    for y in g:
        for x in g[y]:
            if g[y][x] == ',':
                # Expand
                if g[y-1][x] == '.':
                    expanded.append([y-1, x])
                elif len(g[y-1][x]) > 1:
                    p = g[y-1][x]
                    if portals[p][0] == [x, y-1]:
                        print('At ' + str(portals[p][0]) + ' expand ' + str(portals[p][1]))
                        expanded.append([portals[p][1][1], portals[p][1][0]])
                    else:
                        print('At ' + str(portals[p][1]) + ' expand ' + str(portals[p][0]))
                        expanded.append([portals[p][0][1], portals[p][0][0]])

                if g[y+1][x] == '.':
                    expanded.append([y+1, x])
                elif len(g[y+1][x]) > 1:
                    p = g[y+1][x]
                    if portals[p][0] == [x, y+1]:
                        print('At ' + str(portals[p][0]) + ' expand ' + str(portals[p][1]))
                        expanded.append([portals[p][1][1], portals[p][1][0]])
                    else:
                        print('At ' + str(portals[p][1]) + ' expand ' + str(portals[p][0]))
                        expanded.append([portals[p][0][1], portals[p][0][0]])

                if g[y][x-1] == '.':
                    expanded.append([y, x-1])
                elif len(g[y][x-1]) > 1:
                    p = g[y][x-1]
                    if portals[p][0] == [x-1, y]:
                        print('At ' + str(portals[p][0]) + ' expand ' + str(portals[p][1]))
                        expanded.append([portals[p][1][1], portals[p][1][0]])
                    else:
                        print('At ' + str(portals[p][1]) + ' expand ' + str(portals[p][0]))
                        expanded.append([portals[p][0][1], portals[p][0][0]])

                if g[y][x+1] == '.':
                    expanded.append([y, x+1])
                elif len(g[y][x+1]) > 1:
                    p = g[y][x+1]
                    if portals[p][0] == [x+1, y]:
                        print('At ' + str(portals[p][0]) + ' expand ' + str(portals[p][1]))
                        expanded.append([portals[p][1][1]], [portals[p][1][0]])
                    else:
                        print('At ' + str(portals[p][1]) + ' expand ' + str(portals[p][0]))
                        expanded.append([portals[p][0][1]], [portals[p][0][0]])

    if len(expanded) > 0:
        for p in expanded:
            g[p[0]][p[1]] = ','
        return [g, False]
    else:
        return [g, True]

if __name__ == "__main__":
    main()
