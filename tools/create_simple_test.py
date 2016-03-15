from graph_gen import *
import json

def main():
	n = 15
	for i in range(3, n):
		with open(r"..\maps\random_%d_%d" % (i, 1), "w") as map_file:
			print r"writing ..\maps\random_%d_%d ... " % (i, 1)
			json.dump(wrap_graph_to_VRP(create_random_graph(i), i, 1, 0, 100), map_file)

if __name__ == "__main__":
	main()