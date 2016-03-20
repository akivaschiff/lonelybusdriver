from graph_gen import *
import json

def main():
	n = 15
	for i in range(1, n):
		with open(r"..\maps\grid_10_1_pss_%d" % i, "w") as map_file:
			print r"..\maps\grid_10_1_pss_%d" % i
			V, E = create_grid2d_graph(10)
			json.dump(wrap_grid_graph(V, E, 1, i), map_file)


def main2():
	n = 15
	for i in range(1, n):
		with open(r"..\maps\mesh_%d_%d" % (i, 3), "w") as map_file:
			print r"writing ..\maps\mesh_%d_%d ... " % (i, 3)
			json.dump(wrap_graph_to_VRP(create_mesh_graph(i), 0, 3), map_file)


if __name__ == "__main__":
	main()