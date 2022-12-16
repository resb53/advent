#!/usr/bin/env python3

import argparse
import sys
import networkx as nx
import re
import copy
from itertools import combinations

# Check correct usage
parser = argparse.ArgumentParser(description="Parse some data.")
parser.add_argument('input', metavar='input', type=str,
                    help='Input data file.')
args = parser.parse_args()

data = []


# Parse the input file
def parseInput(inp):
    try:
        input_fh = open(inp, 'r')
    except IOError:
        sys.exit("Unable to open input file: " + inp)

    for line in input_fh:
        match = re.match(r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)\n$", line)

        if match is not None:
            data.append([match[1], int(match[2]), match[3].split(", ")])


# Build cave map - it's never worth stopping at or turning on a valve when the valve = 0
def caveMap():
    G = nx.Graph()
    zeroes = []

    for paths in data:
        G.add_node(paths[0], flow=paths[1])
        G.add_edges_from([(paths[0], x, {"weight": 1}) for x in paths[2]])

    for node in G.nodes():
        if node != "AA" and G.nodes[node]["flow"] == 0:
            zeroes.append(node)

    for node in zeroes:
        for connect in combinations(G.neighbors(node), 2):
            if connect not in G.edges():
                G.add_edge(connect[0], connect[1], weight=nx.shortest_path_length(G, connect[0], connect[1], "weight"))
            else:
                print(f"Check {connect}")
        G.remove_node(node)

    return G


# Find route that releases the most pressure in 30 minutes
def processData(caves: nx.Graph):
    routes = [["AA", 0, 0, 0, set(caves.nodes())]]
    routes[0][4].remove("AA")
    results = []
    maxtime = 30

    for _ in range(len(caves.nodes())):
        previous = routes
        routes = []
        for route in previous:
            if len(route[4]) > 0:
                for node in route[4]:
                    elapsed = nx.shortest_path_length(caves, route[0], node, "weight") + 1
                    time = route[1] + elapsed
                    if time > maxtime:
                        results.append(route[2] + ((maxtime - route[1]) * route[3]))
                    else:
                        released = route[2] + route[3] * elapsed
                        notopen = copy.deepcopy(route[4])
                        notopen.remove(node)
                        flow = route[3] + caves.nodes[node]["flow"]
                        routes.append([node, time, released, flow, notopen])
            else:
                results.append(route[2] + ((maxtime - route[1]) * route[3]))

    print(f"Part 1: {max(results)}")


# Work with an elephant for 26 minutes
def processMore(caves: nx.Graph):
    routes = [[["AA", 0], ["AA", 0], 0, 0, 0, set(caves.nodes())]]
    routes[0][5].remove("AA")
    results = []
    maxtime = 26

    for depth in range(len(caves.nodes())):
        print(f"{depth + 1}/{len(caves.nodes())}...")
        previous = routes
        routes = []
        for route in previous:
            # Advance time by shortest distance moved/opened
            advance = min(route[0][1], route[1][1], maxtime - route[2])
            me = [route[0][0], route[0][1] - advance]
            ele = [route[1][0], route[1][1] - advance]
            time = route[2] + advance
            released = route[3] + route[4] * advance
            flow = route[4]
            if me[1] == 0:
                flow += caves.nodes[me[0]]["flow"]
            if ele[1] == 0:
                flow += caves.nodes[ele[0]]["flow"]
            # Check time
            if time >= maxtime:
                results.append(route[3] + ((maxtime - route[2]) * route[4]))
            # Get new destinations
            else:
                if ele[1] != 0:
                    if len(route[5]) > 0:
                        done = False
                        for node in caves.neighbors(me[0]):
                            if node in route[5]:
                                done = True
                                notopen = copy.deepcopy(route[5])
                                notopen.remove(node)
                                path = [node, nx.shortest_path_length(caves, me[0], node, "weight") + 1]
                                routes.append([path, ele, time, released, flow, notopen])
                        if not done:
                            for node in route[5]:
                                notopen = copy.deepcopy(route[5])
                                notopen.remove(node)
                                path = [node, nx.shortest_path_length(caves, me[0], node, "weight") + 1]
                                routes.append([path, ele, time, released, flow, notopen])
                    else:
                        routes.append([["Done", maxtime], ele, time, released, flow, set()])
                elif me[1] != 0:
                    if len(route[5]) > 0:
                        done = False
                        for node in caves.neighbors(ele[0]):
                            if node in route[5]:
                                done = True
                                notopen = copy.deepcopy(route[5])
                                notopen.remove(node)
                                path = [node, nx.shortest_path_length(caves, ele[0], node, "weight") + 1]
                                routes.append([me, path, time, released, flow, notopen])
                        if not done:
                            for node in route[5]:
                                notopen = copy.deepcopy(route[5])
                                notopen.remove(node)
                                path = [node, nx.shortest_path_length(caves, ele[0], node, "weight") + 1]
                                routes.append([me, path, time, released, flow, notopen])
                    else:
                        routes.append([me, ["Done", maxtime], time, released, flow, set()])
                else:
                    if len(route[5]) > 1:
                        for pair in combinations(route[5], 2):
                            notopen = copy.deepcopy(route[5])
                            notopen.remove(pair[0])
                            notopen.remove(pair[1])
                            a = [pair[0], nx.shortest_path_length(caves, me[0], pair[0], "weight") + 1]
                            b = [pair[1], nx.shortest_path_length(caves, ele[0], pair[1], "weight") + 1]
                            routes.append([a, b, time, released, flow, notopen])

                            notopen = copy.deepcopy(notopen)
                            c = [pair[1], nx.shortest_path_length(caves, me[0], pair[1], "weight") + 1]
                            d = [pair[0], nx.shortest_path_length(caves, ele[0], pair[0], "weight") + 1]
                            routes.append([c, d, time, released, flow, notopen])
                    elif len(route[5]) == 1:
                        path = list(route[5])[0]
                        a = [path, nx.shortest_path_length(caves, me[0], pair[1], "weight") + 1]
                        b = [path, nx.shortest_path_length(caves, ele[0], pair[1], "weight") + 1]
                        routes.append([a, ["Done", maxtime], time, released, flow, set()])
                        routes.append([["Done", maxtime], b, time, released, flow, set()])
                    elif len(route[5]) == 0:
                        results.append(released + ((maxtime - time - 1) * flow))

    print(f"Part 2: {max(results)}")


def main():
    parseInput(args.input)
    caves = caveMap()

    # Part 1
    processData(caves)

    # Part 2
    processMore(caves)


if __name__ == "__main__":
    main()
