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
    printGrid(grid)
    getPortals()
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

def getPortals():
    global grid, portals, pos
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
                            portals[p].append([v[1], v[0]])
                            grid[v[0]][v[1]] = p
                            grid[v[2]][v[3]] = ' '

def calcRoutes():
    global grid
    count = 0
    grid[pos[1]][pos[0]] = '█'
    done = False

    while done == False:
        count += 1
        grid, done = expand(grid)

        #if count % 20 == 0:
        #    printGrid(grid)

    return(count)

def expand(g):
    # No bound checking as surrounding wall
    expanded = []
    done = False
    for y in g:
        for x in g[y]:
            check = [[y-1, x], [y+1, x], [y, x+1], [y, x-1]]
            if g[y][x] == '█':
                # Expand
                for v in check:
                    if g[v[0]][v[1]] == '.':
                        expanded.append([v[0], v[1], '.'])
                    elif len(g[v[0]][v[1]]) > 1:
                        p = g[v[0]][v[1]]
                        if portals[p][0] == [v[1], v[0]]:
                            expanded.append([portals[p][1][1], portals[p][1][0], 'p'])
                        else:
                            expanded.append([portals[p][0][1], portals[p][0][0], 'p'])
                    elif g[v[0]][v[1]] == '£':
                        done = True

    if len(expanded) > 0:
        for p in expanded:
            if p[2] == '.':
                g[p[0]][p[1]] = '█'
            else:
                expandTile(p[1], p[0])
        return [g, done]
    else:
        return [g, True]

def expandTile(x, y):
    global grid
    for v in [[y-1, x], [y+1, x], [y, x+1], [y, x-1]]:
        if grid[v[0]][v[1]] == '.':
            grid[v[0]][v[1]] = '█'

if __name__ == "__main__":
    main()
