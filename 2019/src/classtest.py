#!/usr/bin/python3

import intCode

def main():
    prog = intCode.Program('inputs/arcade.txt')
    prog.run()

if __name__ == "__main__":
    main()
