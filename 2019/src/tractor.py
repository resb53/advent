#!/usr/bin/python3

import intCode
import argparse
import sys

# Check correct usage
parser = argparse.ArgumentParser(description="Test tractor beam.")
parser.add_argument('code', metavar='code', type=str, help='Int code file.')
args = parser.parse_args()
grid = {}
io = {'inp': [], 'out': []}
sym = {0: '.', 1: '#'}

def main():
    global grid, io

    # part 1
    count = 0
    for y in range(50):
        grid[y] = {}
        for x in range(50):
            io['inp'] = [x, y]
            prog = intCode.Program(args.code)
            prog.run(i=instr_in, o=instr_out)
            grid[y][x] = io['out'].pop(0)
            count += grid[y][x]

    drawGrid(grid)
    print(count)

def instr_out(p):
    global io
    io['out'].append(p)

def instr_in():
    cmd = io['inp'].pop(0)
    return cmd

def drawGrid(g):
    for y in range(0, len(g)):
        for x in range(0, len(g[y])):
            print(sym[grid[y][x]], end='')
        print('')

if __name__ == "__main__":
    main()
