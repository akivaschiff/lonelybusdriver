import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import itertools
import copy
import consts
import random

class Routeset(object):
	def __init__(self, num_routes, transportNetwork):
		self.routes = [[] for _ in range(num_routes)]
		#self._lengths = [0 for _ in range(num_routes)]
		self.transportNetwork = transportNetwork # save a pointer to the original graph
	def add_stop(self, route_num, node):
		self.routes[route_num].append(node)
	def reverse(self, route_num):
		self.routes[route_num].reverse()
	def get_routes(self):
		return self.routes
	def add_route(self, route):
		self.routes.append(copy.copy(route))
	def calc_route_length(self, route):
		return sum([self.transportNetwork.edge[route[j]][route[j+1]]['weight'] for j in range(len(route)-1)])
	def get_operator_cost(self):
		return sum([self.calc_route_length(route) for route in self.routes])
	def get_edges(self, route):
		return [(route[j],route[j+1]) for j in range(len(route)-1)]
	def get_passenger_cost(self, demand):
		# record edges to duplicate
		counter = Counter()
		for route in self.routes:
			counter.update(route)
		duplicates = {i:j for i,j in counter.iteritems() if j > 1}
		incrementor = {i:0 for i,j in duplicates.iteritems()}

		# create new graph
		transitNetwork = nx.Graph()
		for route in self.routes:
			for a, b in self.get_edges(route):
				edge = (str(a), str(b))
				if a in incrementor:
					edge = (str(a) + '_%s' % (chr(97 + incrementor[a])), edge[1])
				if b in incrementor:
					edge = (edge[0], str(b) + '_%s' % (chr(97 + incrementor[b])))
				transitNetwork.add_edge(*edge, weight = self.transportNetwork.edge[a][b]['weight'])
			for r in route:
				if r in incrementor:
					incrementor[r] += 1

		# create transit edges
		for node, appearances in duplicates.iteritems():
			split_nodes = [str(node) + '_' + chr(97 + i) for i in range(appearances)]
			for a, b in itertools.combinations(split_nodes, 2):
				transitNetwork.add_edge(a, b, weight = consts.transfer_penalty)

		old_positions = nx.get_node_attributes(self.transportNetwork, 'pos')
		positions = {n : old_positions[float(n.split('_')[0])] for n in transitNetwork.nodes()}
		nx.draw(transitNetwork, positions, node_size = 800)
		labels = {n:n for n in transitNetwork.nodes()}
		nx.draw_networkx_labels(transitNetwork, positions, labels=labels)
		#plt.show()

		# run all pairs shortest path algorithm
		all_pairs = nx.algorithms.all_pairs_shortest_path_length(transitNetwork)

		# now calculate the sum of all the pairs
		total_sum = 0
		for source, dest in demand:
			if source > dest:
				dest, source = source, dest
			a, b = str(source), str(dest)
			if source not in duplicates and dest not in duplicates:
				total_sum += demand[(source,dest)] * all_pairs[a][b]
			elif source not in duplicates and dest in duplicates:
				split_nodes = [str(b) + '_' + chr(97 + i) for i in range(duplicates[dest] - 1)]
				total_sum += demand[(source,dest)] * min(all_pairs[a][c] for c in split_nodes)
			elif source in duplicates and dest not in duplicates:
				split_nodes = [str(a) + '_' + chr(97 + i) for i in range(duplicates[source] - 1)]
				total_sum += demand[(source,dest)] * min(all_pairs[c][b] for c in split_nodes)
			else:
				# both are duplicated! arghhh!
				split_nodes_a = [str(a) + '_' + chr(97 + i) for i in range(duplicates[dest] - 1)]
				split_nodes_b = [str(b) + '_' + chr(97 + i) for i in range(duplicates[source] - 1)]
				total_sum += demand[(source,dest)] * min(all_pairs[c][d] for c, d in itertools.product(split_nodes_a, split_nodes_b))
		return total_sum




	def show(self):
		positions = nx.get_node_attributes(self.transportNetwork, 'pos')
		nx.draw(self.transportNetwork, positions, node_size = 300)
		labels = {n:n for n in self.transportNetwork.nodes()}
		nx.draw_networkx_labels(self.transportNetwork, positions, labels=labels)
		for i in range(len(self.routes)):
			nx.draw_networkx_edges(self.transportNetwork, positions, edgelist = self.get_edges(self.routes[i]), alpha = 0.2, edge_color = consts.COLORS[i], width = 8)
		plt.show()