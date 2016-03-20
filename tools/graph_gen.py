"""
Graph generator:

usage:
    # create several  graphs
    # 5 nodes:
    with open("5ring1bus.txt", "w") as map_file:
        json.dump(wrap_graph_to_VRP(create_ring_graph(5), 5, 1), map_file)

    with open("5ring3bus.txt", "w") as map_file:
        json.dump(wrap_graph_to_VRP(create_ring_graph(5), 5, 3), map_file)

    with open("5mesh1bus.txt", "w") as map_file:
        json.dump(wrap_graph_to_VRP(create_mesh_graph(5), 5, 1), map_file)

    with open("5mesh3bus.txt", "w") as map_file:
        json.dump(wrap_graph_to_VRP(create_mesh_graph(5), 5, 3), map_file)
"""
import networkx
import argparse
import random
import json


def get_random_position(a, b):
    return random.randint(a, b), random.randint(a, b)


def get_random_node_position(node_name, a, b):
    x, y = get_random_position(a, b)
    return [str(node_name), x, y]


def create_ring_graph(n):
    """
    Creates a ring graph with n nodes.
    returns (V, E)
    """
    assert n > 0
    V = range(n)
    E = {(i, i+1) for i in range(n-1)}
    E.add((n-1, 0))
    return V, E


def create_mesh_graph(n):
    """
    Creates a mesh graph with n nodes.
    returns (V, E)
    """
    assert n > 0 
    V = range(n)
    E = {(i, j) for i in range(n) for j in range(n) if i != j}
    return V, E


def create_star_graph(n):
    raise NotImplemented()


def create_random_graph(n):
    g = networkx.binomial_graph(n, 0.5)
    while not networkx.is_connected(g):
        g = networkx.binomial_graph(n, 0.5)
    return g.nodes(), g.edges()


def create_grid2d_graph(n):
    g = networkx.grid_2d_graph(n, n)
    return g.nodes(), g.edges()


def create_random_passengers(V, pass_number):
    res = []
    for i in range(pass_number):
        v, u = random.sample(V, 2)
        res.append([str(u), str(v)])
    return res


def create_passengers_in_every_station(V, pass_number):
    return [[str(u), str(len(V)-1)] for u in V]


def wrap_grid_graph(V, E, n_busses, pass_number):
    stations = [[str(i), V[i][0], V[i][1]] for i in range(len(V))]
    stations_map = {str(v): str(i) for i, v in enumerate(V)}
    roads = [[stations_map[str(u)], stations_map[str(v)]] for u, v in E]

    return {
        "lines": n_busses,
        "stations": stations,
        "roads": roads,
        "passengers": [[stations_map[u], stations_map[v]] for u, v in create_random_passengers(V, pass_number)]
    }


def wrap_graph_to_VRP(graph, goal, n_busses, a=0, b=100, n_passengers=100):
    assert n_busses > 0
    V, E = graph
    stations = [get_random_node_position(v, a, b) for v in V]
    roads = [[str(v1), str(v2)] for v1, v2 in E]

    return {
        "lines": n_busses,
        "stations": stations,
        "roads": roads,
        "passengers": create_passengers_in_every_station(V)
    }


def main():
    parser = argparse.ArgumentParser(
        description='Graph generator\n example:\n\tpython %s --graph_type mesh --n 10 --g 9 --bus 2 --o 10mesh2bus.txt'
                    % __file__)
    parser.add_argument("--graph_type", help="can be on of the following options: (ring, mesh, star, random)")
    parser.add_argument("--n", help="number of nodes", type=int)
    parser.add_argument("--bus", help="number of bus", type=int)
    parser.add_argument("--g", help="goal (single station)", type=int)
    parser.add_argument("--o", help="output file (map file)")
    parser.add_argument("--a", help="minimal position value", type=int, default=0)
    parser.add_argument("--b", help="maximal position value", type=int, default=100)

    graph_function = {
        'ring': create_ring_graph,
        'mesh': create_mesh_graph,
        'star': create_star_graph,
        'random': create_random_graph,
        'grid2d': create_grid2d_graph
    }

    args = parser.parse_args()
    assert args.a < args.b
    assert args.graph_type in graph_function
    with open(args.o, "w") as map_file:
        json.dump(wrap_graph_to_VRP(graph_function[args.graph_type](args.n), args.g, args.bus, args.a, args.b),
                  map_file)

if __name__ == "__main__":
    main()

