#!/usr/bin/python3

import intcode

pos = [0,0,0] # x,y,bearing - 0 North, 1 East, 2, South, 3 West
grid = {'0,0': 0} # x,y -> 0 black, 1 white
io = {"input": [1], "output": []} # Dict holding next input / last output

def main():
    global grid
    # Prepare intcode computer
    intcode.init('inputs/painting.txt')
    intcode.run(i=instr_in, o=instr_out)
    # How many panels painted at least once?
    # print(len(grid))
    paintID()

def instr_in():
    global pos, grid, io

    # Prepare next input and implement output
    if len(io['output']) > 0:
        loc = str(pos[0]) + ',' + str(pos[1])
        drn = pos[2]
        # Paint
        grid[loc] = io['output'].pop(0)
        # Turn
        if io['output'][0] == 0:
            io['output'][0] = -1
        drn = (drn + io['output'].pop(0)) % 4
        # Move
        if drn == 0:
            pos[1] -= 1
        elif drn == 1:
            pos[0] += 1
        elif drn == 2:
            pos[1] += 1
        else: #drn = 3
            pos[0] -= 1
        # Update
        pos[2] = drn
        loc = str(pos[0]) + ',' + str(pos[1])
        # Read/send to input
        if loc not in grid:
            io['input'].append(0)
        else:
            io['input'].append(grid[loc])

    return io['input'].pop(0)

def instr_out(p):
    global io

    io['output'].append(p)

def paintID():
    global grid
    # Produce a y/x nested dict from grid
    pic = {}
    minx = 100
    maxx = -100
    miny = 100
    maxy = -100

    for c in grid:
        x, y = c.split(',')
        x = int(x)
        if x > maxx:
            maxx = x
        if x < minx:
            minx = x
        y = int(y)
        if y > maxy:
            maxy = y
        if y < miny:
            miny = y

        if y not in pic:
            pic[y] = {}
        pic[y][x] = grid[c]

    # Iterate through painting
    for y in range(miny,maxy+1):
        if y not in pic:
            pic[y] = {}
        for x in range(minx,maxx+1):
            if x not in pic[y]:
                pic[y][x] = 0
            if pic[y][x] == 0:
                print(' ',end='')
            else:
                print('█',end='')
        print('')

if __name__ == "__main__":
    main()
