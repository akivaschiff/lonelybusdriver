from graph_gen import *
import json

def main():
	n = 20
	for i in range(1, n):
		with open(r"..\maps\many\grid_pss_%d" % i, "w") as map_file:
			V, E = create_grid2d_graph(15)
			json.dump(wrap_grid_graph(V, E, max(3, i / 4), i), map_file)


def main2():
	n = 20
	for i in range(1, n):
		with open(r"..\maps\many\mesh_20_%d" % i, "w") as map_file:
			json.dump(wrap_graph_to_VRP(create_mesh_graph(20), 0, max(3, i / 4), n_passengers=i), map_file)


if __name__ == "__main__":
	main2()