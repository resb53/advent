#!/usr/bin/python3

import intCode

pos = [0,0,0] # x,y,bearing - 0 North, 1 East, 2, South, 3 West
grid = {} # grid[y][x] -> 0 empty, 1 wall, 2 block, 3 paddle, 4 ball
io = {"input": [1], "output": []} # Dict holding next input / last output
char = {0: ' ', 1: '|', 2: '█', 3:'_', 4:'o'}
score = 0

def main():
    global grid
    # Prepare intcode computer
    intCode.init('inputs/cheatarcade.txt')
    intCode.run(i=instr_in,o=instr_out)
    # Output
    #draw(grid)
    print(score)

def instr_out(p):
    global io, grid, score

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

def instr_in():
    return 0

def draw(g):
    for y in sorted(g):
        for x in sorted(g[y]):
            print(char[g[y][x]], end='')
        print('')

#def cheat(mem):
    #for i in range(0,len(mem)-2):
        #if mem[i] == 0 and mem[i+1] == 3 and mem[i+2] == 0:
            #Convert all of the paddle row into walls
            #for j in range(i-19,i+21):
                # Write 1 to each j location

if __name__ == "__main__":
    main()
