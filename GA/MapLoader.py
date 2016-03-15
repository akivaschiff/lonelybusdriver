import networkx as nx
import matplotlib.pyplot as plt
import pprint
import os

def parse_map(map_name):
	suffixes = ['Coords','Demand','TravelTimes']
	files = [os.path.join(os.path.dirname(os.path.abspath(__file__)),'maps',map_name + i + '.txt') for i in suffixes]
	# read coordinates
	TransportNetwork = nx.Graph()

	coords = file(files[0],'r').read().splitlines()
	for count in range(int(coords[0])):
		x,y = [float(i) for i in coords[count+1].split(' ')]
		TransportNetwork.add_node(count, pos = (x,y))


	# read traveltimes
	lines = [line for line in file(files[2],'r').read().splitlines() if line]
	for i, line in enumerate(lines):
		columns = line.split()
		for j, col in enumerate(columns):
			if col != '0' and col != 'Inf':
				TransportNetwork.add_edge(i,j,weight = float(col))

	# read demand
	demand = {}
	lines = [line for line in file(files[1],'r').read().splitlines() if line]
	for i, line in enumerate(lines):
		columns = line.split()
		for j, col in enumerate(columns):
			num = float(col)
			if num == 0 or i > j:
				continue
			demand[(i,j)] = num # consider duplicating this to easily  access both directions (i,j) = (j,i)

	#print TransportNetwork.edges(data = True)
	return TransportNetwork, demand

def main(map_name, show = True):
	transportNetwork, demand = parse_map(map_name)

	if show == True:
		positions = nx.get_node_attributes(transportNetwork, 'pos')
		nx.draw(transportNetwork, positions, node_size = 300)
		labels = {n:n for n in transportNetwork.nodes()}
		nx.draw_networkx_labels(transportNetwork, positions, labels=labels)
		plt.show()

if __name__ == '__main__':
	map_name = "Mandl"
	main(map_name, True)