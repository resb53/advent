#!/usr/bin/python3

import intCode

pos = [0,0,0] # x,y,bearing - 0 North, 1 East, 2, South, 3 West
grid = {} # grid[y][x] -> 0 empty, 1 wall, 2 block, 3 paddle, 4 ball
io = {'input': [], 'output': []} # Dict holding next input / last output
char = {0: ' ', 1: '|', 2: '█', 3:'_', 4:'o'}
score = 0
ballpos = [0,0] # [x,y]
paddpos = [0,0]

def main():
    global grid
    # Prepare intcode computer
    prog = intCode.Program('inputs/arcade.txt')
    # insert coin
    prog.mem[0] = 2
    prog.run(i=instr_in,o=instr_out)
    # Output
    print(score)

def instr_out(p):
    global io, grid, score, ballpos, paddpos

    io['output'].append(p)

    if len(io['output']) == 3:
        x = io['output'].pop(0)
        y = io['output'].pop(0)
        v = io['output'].pop(0)
        if x == -1 and y == 0:
            score = v
        else:
            if y not in grid:
                grid[y] = {}
            grid[y][x] = v
            # Update paddpos or ballpos
            if v == 3:
                paddpos = [x,y]
            elif v == 4:
                ballpos = [x,y]
                movePaddle()

def movePaddle():
    if paddpos[0] < ballpos[0]:
        io['input'].append(1)
    elif paddpos[0] == ballpos[0]:
        io['input'].append(0)
    else:
        io['input'].append(-1)

def instr_in():
    return io['input'].pop(0)

def draw(g):
    for y in sorted(g):
        for x in sorted(g[y]):
            print(char[g[y][x]], end='')
        print('')

if __name__ == "__main__":
    main()
