#!/usr/bin/python3

import intcode

pos = [0,0,0] # x,y,bearing - 0 North, 1 East, 2, South, 3 West
grid = {'0,0': 0} # x,y -> 0 empty, 1 wall, 2 block, 3 paddle, 4 ball
io = {"input": [1], "output": []} # Dict holding next input / last output

def main():
    global grid
    # Prepare intcode computer
    intcode.init('inputs/arcade.txt')
    intcode.run(o=instr_out)
    # Output
    # print(grid)
    count = 0
    for tile in grid:
        if grid[tile] == 2:
            count += 1
    print(count)

def instr_out(p):
    global io

    io['output'].append(p)

    if len(io['output']) == 3:
        grid[str(io['output'][0]) + ',' + str(io['output'][1])] = io['output'][2]
        io['output'] = []

if __name__ == "__main__":
    main()
