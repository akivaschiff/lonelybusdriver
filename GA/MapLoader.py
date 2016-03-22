import networkx as nx
import matplotlib.pyplot as plt
import glob
import sys
import os

'''
This file contains logic for parsing the map formats into networkx Graph objects and a Demand matrix
'''

def parse_map(map_name):
	suffixes = ['Coords','Demand','TravelTimes']
	files = [os.path.join(os.path.dirname(os.path.abspath(__file__)),'maps',map_name + i + '.txt') for i in suffixes]
	# read coordinates
	TransportNetwork = nx.Graph()

	coords = file(files[0],'r').read().splitlines()
	for count in range(int(coords[0])):
		x,y = [float(i) for i in coords[count+1].strip().split()]
		TransportNetwork.add_node(count+1, pos = (x,y))

	# read traveltimes - edges
	lines = [line for line in file(files[2],'r').read().splitlines() if line]
	for i, line in enumerate(lines):
		columns = line.split()
		for j, col in enumerate(columns):
			if col != '0' and col != 'Inf':
				TransportNetwork.add_edge(i+1,j+1,weight = float(col))

	# read demand
	demand = {}
	lines = [line for line in file(files[1],'r').read().splitlines() if line.strip()]
	for i, line in enumerate(lines):
		columns = line.split()
		for j, col in enumerate(columns):
			num = float(col)
			if num == 0 or i > j:
				continue
			demand[(i+1,j+1)] = num # consider duplicating this to easily  access both directions (i,j) = (j,i)

	#print TransportNetwork.edges(data = True)
	setattr(TransportNetwork, "demand", demand)
	setattr(TransportNetwork, "dij_sum", float(sum(demand.values())))
	return TransportNetwork

def main(map_name, show = True):
	transportNetwork = parse_map(map_name)

	if show == True:
		positions = nx.get_node_attributes(transportNetwork, 'pos')
		nx.draw(transportNetwork, positions, node_size = 300)
		labels = {n:n for n in transportNetwork.nodes()}
		nx.draw_networkx_labels(transportNetwork, positions, labels=labels)
		plt.show()

if __name__ == '__main__':
	if not os.path.exists('maps'):
		print 'MAP FOLDER NOT FOUND'
		sys.exit(0)

	map_names = [name.split(os.path.sep)[1].split('Coords')[0] for name in glob.glob(os.path.join('maps','*Coords*'))]
	if len(sys.argv) < 2 or sys.argv[1] not in map_names:
		print "Usage: MapLoader.py <map_name>\nName should be one of %s" % str(map_names)
		sys.exit(0)

	map_name = sys.argv[1]
	main(map_name, True)