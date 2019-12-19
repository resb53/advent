#!/usr/bin/python3

import intCode
import argparse
import sys
from collections import deque

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
    #count = 0
    #for y in range(50):
    #    grid[y] = {}
    #    for x in range(50):
    #        io['inp'] = [x, y]
    #        prog = intCode.Program(args.code)
    #        prog.run(i=instr_in, o=instr_out)
    #        grid[y][x] = io['out'].pop(0)
    #        count += grid[y][x]

    #drawGrid(grid)
    #print(count)

    # part 2
    # Look for leading, following edge pattern
    for y in range(600,601): # Start at row 2 to avoid blank lines
        beam = 0
        x = -1
        print('y:' + str(y), end='')
        while beam != 2:
            x += 1
            io['inp'] = [x, y]
            prog = intCode.Program(args.code)
            prog.run(i=instr_in, o=instr_out)
            test = io['out'].pop(0)
            if beam == 0 and test == 1:
                beam += 1
                print('; start:' + str(x), end='')
            elif beam == 1 and test == 0:
                beam += 1
                print('; end:' + str(x-1))

#y:3; start:2; end:2
#y:4; start:3; end:3
#y:5; start:4; end:4
#y:6; start:4; end:5
#y:7; start:5; end:5
#y:8; start:6; end:6
#y:9; start:6; end:7
#y:10; start:7; end:8
#y:11; start:8; end:9
#y:12; start:8; end:10
#y:13; start:9; end:10
#y:14; start:10; end:11
#y:15; start:10; end:12
#y:16; start:11; end:13
#y:17; start:12; end:14
#y:18; start:12; end:15
#y:19; start:13; end:15
#y:20; start:14; end:16

    # Part 2 calculation
    done = 0
    y=8 # Start at 8, easier patterns
    start=6
    end=6
    n=0
    initial = [{'y': y, 'start': 6, 'end': 6}]
    cache = deque(initial, maxlen=99)

    while done == 0:
        y += 1
        n += 1

        if n % 3 != 1:
            start += 1
        if n % 6 != 5:
            end += 1

        # Debug
        if y == 600:
            print('y:' + str(y) + '; start:' + str(start) + '; end:' + str(end))

        new = {'y': y, 'start': start, 'end': end}
        # Cache 100 rows ago, and see if old end - new start = 99
        if cache[0]['end'] - start >= 99:
            done = 1
            print('Old: ' + str(cache[0]))
            print('New: ' + str(new))
            print('Answer: ' + str(cache[0]['start'] * 10000 + cache[0]['y']))
        else:
            cache.append(new)

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
