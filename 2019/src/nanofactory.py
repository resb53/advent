#!/usr/bin/python3

import sys
import argparse

# Globals
menu = {'ORE': [1, {'ORE': 1}]} # 1 ORE always requires 1 ORE

def main():
    # Check correct usage
    parser = argparse.ArgumentParser(description="Nanofactory material calculator.")
    parser.add_argument('ingredients', metavar='ingredients_file', type=str, help='Specify the ingredients for the recipe.')
    args = parser.parse_args()

    init(args.ingredients)
    # Menu ready
    print(menu)
    calculateOre()


def init(fh):
    global menu
    # Parse memory
    try:
        instr_fh = open(fh,'r')
    except IOError:
        sys.exit("Unable to open input file: " + fh)

    # Parse instructions in file. Allow for multiline just in case future need.
    for line in instr_fh:
        line = line.strip('\n')

        # Parse line
        mats, result = line.split(' => ')
        qr, result = result.split(' ')

        mix = {}
        for mat in mats.split(', '):
            qm, mat = mat.split(' ')
            mix[mat] = int(qm)

        menu[result] = [int(qr), mix]

def calculateOre():
    global menu
    # Count numbers required
    shoplist = {'FUEL': 1}

    #Get 1 FUEL
    while list(shoplist.keys()) != ['ORE']:
        print( str(list(shoplist.keys())) + ' vs ' + str(['ORE']) )
        print('S:' + str(shoplist))
        newlist = {}
        for item in shoplist:
            print(item)
            for ing in menu[item][1]:
                if ing in newlist:
                    newlist[ing] += shoplist[item] * menu[item][1][ing]
                else:
                    newlist[ing] = shoplist[item] * menu[item][1][ing]
            print(newlist)
        shoplist = newlist

    print(shoplist)


if __name__ == "__main__":
    main()
