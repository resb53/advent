#!/usr/bin/python3

import intCodeClass
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
    #        prog = intCodeClass.Program(args.code)
    #        prog.run(i=instr_in, o=instr_out)
    #        grid[y][x] = io['out'].pop(0)
    #        count += grid[y][x]

    #drawGrid(grid)
    #print(count)

    # part 2
    debug = {} # {y: [[start, end], [genstart, genend]]

    # No pattern but have estimate range
    initial = [{'y': 3, 'start': 2, 'end': 2}]
    cache = deque(initial, maxlen=99)
    for y in range(4,1100): # Start at row 2 to avoid blank lines
        beam = 0
        x = cache[-1]['start']-2 #Start at where the last rows first # was seen
        start = 0
        end = 0
        print('y:' + str(y))
        while beam != 2:
            x += 1
            print(str(x) + ':', end='')
            io['inp'] = [x, y]
            prog = intCodeClass.Program(args.code)
            prog.run(i=instr_in, o=instr_out)
            test = io['out'].pop(0)
            print(str(test) + '; ', end='')
            if beam == 0 and test == 1:
                beam += 1
                start = x
                # Skip forwards towards last # could be 1 less than last width
                if y > 20:
                    x += (cache[-1]['end'] - cache[-1]['start'] - 2)
            elif beam == 1 and test == 0:
                beam += 1
                end = x-1
                new = {'y': y, 'start': start, 'end': end}
                print('\n' + str(new))
                # Cache 100 rows ago, and see if old end - new start = 99
                if cache[0]['end'] - start >= 99:
                    print('Old: ' + str(cache[0]))
                    print('New: ' + str(new))
                    print('Answer: ' + str((cache[0]['end'] - 99) * 10000 + cache[0]['y']))
                    sys.exit(0)
                else:
                    cache.append(new)


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
    #done = 0
    #y=8 # Start at 8, easier patterns
    #start=6
    #end=6
    #n=0
    #initial = [{'y': y, 'start': 6, 'end': 6}]
    #cache = deque(initial, maxlen=99)

    #while done == 0:
    #    y += 1
    #    n += 1

    #    if n % 3 != 1:
    #        start += 1
    #    if n % 6 != 5:
    #        end += 1

    #    # Debug
    #    if y >= 10 and y < 61:
    #        #print('y:' + str(y) + '; start:' + str(start) + '; end:' + str(end))
    #        debug[y].append([start, end])

    #    new = {'y': y, 'start': start, 'end': end}
    #    # Cache 100 rows ago, and see if old end - new start = 99
    #    if cache[0]['end'] - start >= 99:
    #        done = 1
    #        print('Old: ' + str(cache[0]))
    #        print('New: ' + str(new))
    #        print('Answer: ' + str(cache[0]['start'] * 10000 + cache[0]['y']))
    #    else:
    #        cache.append(new)

    #print("Debug:")
    #for y in debug:
    #    print("y:" + str(y) + "; intcode:" + str(debug[y][0]) + "; pregen:" + str(debug[y][1]))

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
