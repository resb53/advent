#!/usr/bin/python3

import intcode

def main():
    # Prepare intcode computer
    intcode.init('inputs/boost.txt')
    intcode.run()

if __name__ == "__main__":
    main()
