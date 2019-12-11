#!/usr/bin/python3

import intcode

pos = [0,0,0] # x,y,bearing - 0 North, 1 East, 2, South, 3 West
grid = {'0,0': 0} # x,y -> 0 black, 1 white
io = {"input": [0], "output": []} # Dict holding next input / last output

def main():
    global grid
    # Prepare intcode computer
    intcode.init('inputs/painting.txt')
    intcode.run(i=instr_in, o=instr_out)
    # How many panels painted at least once?
    print(len(grid))

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


if __name__ == "__main__":
    main()
