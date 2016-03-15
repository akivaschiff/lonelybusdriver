import networkx as nx
import os



def main(map_name):
	suffixes = ['Coords','Demand','TravelTimes']
	files = [os.path.join(os.path.dirname(os.path.abspath(__file__)),'maps',map_name + i + '.txt') for i in suffixes]
	# read coordinates
	TransportNetwork = nx.Graph()

	coords = file(files[0],'r').read().splitlines()
	for count in range(int(coords[0])):
		x,y = [float(i) for i in coords[count+1].split(' ')]
		TransportNetwork.add_node(count, x = x, y = y)

	print TransportNetwork.nodes(data = True)

	# read traveltimes
	lines = file(files[2],'r').read().splitlines()
	for i in range(len(lines)):
		delim = '\t' if '\t' in lines[i] else ' ' * 4
		in_line = lines.split(delim)
		for j in range(len(in_line)):
			


if __name__ == '__main__':
	map_name = "Mandl"
	main(map_name)