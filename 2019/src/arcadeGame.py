#!/usr/bin/python3

import intCodeClass
import curses
import sys
import time

pos = [0,0,0] # x,y,bearing - 0 North, 1 East, 2, South, 3 West
grid = {} # grid[y][x] -> 0 empty, 1 wall, 2 block, 3 paddle, 4 ball
io = {'input': [], 'output': []} # Dict holding next input / last output
char = {0: ' ', 1: '|', 2: '█', 3:'_', 4:'o'}
score = 0
ballpos = [0,0] # [x,y]
paddpos = [0,0]

def main():
    global grid, game
    # Prepare screen
    win = curses.initscr()
    win.clear()
    win.refresh()
    game = curses.newwin(25, 43, 5, 10)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    # Prepare intcode computer
    prog = intCodeClass.Program('inputs/arcade.txt')
    # insert coin
    prog.mem[0] = 2
    prog.run(i=instr_in,o=instr_out)
    # Hold then reset screen
    game.addstr(23, 10, "You win! Your score:")
    game.refresh()
    time.sleep(3)
    curses.endwin()

def instr_out(p):
    global io, grid, score, ballpos, paddpos, game

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
                # Update screen
                game.addstr(0, 0, draw(grid))
                game.addstr(24, 19, str(score))
                game.refresh()
                time.sleep(.02)

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
    image = ''
    for y in sorted(g):
        for x in sorted(g[y]):
            image += char[g[y][x]]
        image += '\n'
    return image

if __name__ == "__main__":
    main()
