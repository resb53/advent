#!/usr/bin/python3

import sys
import argparse

# Globals
menu = {}

def main():
    # Check correct usage
    parser = argparse.ArgumentParser(description="Nanofactory material calculator.")
    parser.add_argument('ingredients', metavar='ingredients_file', type=str, help='Specify the ingredients for the recipe.')
    args = parser.parse_args()

    init(args.ingredients)
    # Menu ready
    recipe = calculateOre()
    recipe = orderRecipe(recipe)
    #printRecipe(recipe)
    # Use recipe
    cook(recipe)


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
    # Count numbers required
    shoplist = {'FUEL': 1}
    recipe = [] # Production recipe to follow
    leftover = {} # Remaining components
    ore = 0 # Ore required
    #Get 1 FUEL
    while len(shoplist) > 0:
        #print('S:' + str(shoplist))
        newlist = {}
        for item in shoplist:
            #print(item)
            prod = 0 # items made of this
            # See if we have any already
            if item in leftover:
                if leftover[item] >= shoplist[item]:
                    leftover[item] -= shoplist[item]
                    shoplist[item] = 0
                else:
                    shoplist[item] -= leftover[item]
                    leftover[item] = 0
                #print('Used leftovers - ' + 'Req: ' + str(shoplist[item]) + 'Left: ' + str(leftover[item]))
            if shoplist[item] > 0:
                for ing in menu[item][1]:
                    #print('<' + ing)
                    # Check for any leftovers
                    avail = 0
                    if ing in leftover:
                        avail = leftover[ing]
                    # Get most efficient production from menu
                    [prod, req, left] = getReq(shoplist[item], menu[item][1][ing], menu[item][0], avail)
                    if ing in leftover:
                        leftover[ing] = left
                    # Update lists
                    if ing == 'ORE':
                        ore += req
                    else:
                        if req > 0:
                            if ing in newlist:
                                newlist[ing] += req
                            else:
                                newlist[ing] = req
                # Calculate leftovers
                if prod > shoplist[item]:
                    if item in leftover:
                        leftover[item] += prod - shoplist[item]
                    else:
                        leftover[item] = prod - shoplist[item]
            # If existing already, add to it, and bring forwards <- doesn't quite order as intended, just add
            i = -1
            for x in range(0,len(recipe)):
                if recipe[x][0] == item:
                    i = x
            if i >= 0:
                #x = recipe.pop(i)
                #x[1] += prod
                recipe[i][1] += prod
                #recipe.insert(i,x)
            else:
                recipe.insert(0,[item, prod])
        shoplist = newlist
        #print('L:' + str(leftover))

    # PART ONE
    #print('ORE required: ' + str(ore))
    #print('Leftovers: ' + str(leftover))

    return recipe

def getReq(req, need, prod, avail):
    #print('Req: ' + str(req) + '; Need: ' + str(need) + '; Prod: ' + str(prod) + '; Avail: ' + str(avail))
    used = 0
    done = 0
    while done < req:
        used += need
        done += prod
    new = 0
    if used >= avail:
        new = used - avail
        avail = 0
    else:
        avail -= used

    #print('Use: ' + str(used) + ' to make ' + str(done) + '. Require: ' + str(new) + ' new and ' + str(avail) + ' leftover.')

    return [done, new, avail]

def orderRecipe(recipe):
    seen = ['ORE']
    ordered = []
    while len(ordered) < len(recipe):
        for instr in recipe:
            # if not already 'made'
            if instr[0] not in seen:
                mats = 0
                for mat in menu[instr[0]][1]:
                    if mat in seen:
                        mats += 1
                if mats == len(menu[instr[0]][1]):
                    #We have the mats, let's cook
                    ordered.append(instr)
                    seen.append(instr[0])
    return ordered

def printRecipe(recipe):
    for entry in recipe:
        print('Produce ' + str(entry[1]) + ' of ' + entry[0] + ' using:', end='')
        crafts = entry[1] // menu[entry[0]][0]
        for ing in menu[entry[0]][1]:
            print(' ' + str(crafts * menu[entry[0]][1][ing]) + ' ' + ing + ',', end='')
        print('')

def cook(recipe):
    # Have a bag of goodies and cook up that tasty fuel
    bag = {'ORE': 1000000000000}
    #bag = {'ORE': 300000}
    lp = 1000000000000 # last print
    i = 10000000000 # print iterator
    while bag['ORE'] > 0:
        if len(bag) == 2:
            print(bag)
        if bag['ORE'] <= lp -i:
            print(bag)
            lp -= i
        for instr in recipe:
            # See if we have enough already
            if instr[0] in bag and instr[0] != 'FUEL' and bag[instr[0]] >= instr[1]:
                #print('Already enough ' + instr[0] + ' in bag.')
                q = 0
            else:
                #print('Cooking: ' + str(instr[1]) + ' ' + str(instr[0]) + ' using: ' + str(menu[instr[0]]))
                for mat in menu[instr[0]][1]:
                    req = instr[1] // menu[instr[0]][0] * menu[instr[0]][1][mat]
                    if mat in bag:
                        bag[mat] -= req
                        #print ('- Used ' + str(req) + ' ' + mat)
                        if bag[mat] < 0:
                            sys.exit('Not enough ' + mat + ' in bag.\nBag: ' + str(bag))
                    else:
                        sys.exit('No ' + mat + ' in bag.')
                # crafted
                if instr[0] not in bag:
                    bag[instr[0]] = instr[1]
                else:
                    bag[instr[0]] += instr[1]
                #print('& Bag: ' + str(bag))

if __name__ == "__main__":
    main()
