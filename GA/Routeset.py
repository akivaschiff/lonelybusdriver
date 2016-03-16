import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import itertools
import pprint
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
	def _generate_name(self, node, inc):
		return '%s_%s' % (node, chr(97 + inc))
	def _generate_names(self, node, number):
		return [self._generate_name(node, inc) for inc in range(number)]
	def get_passenger_cost(self, demand):
		# record edges to duplicate
		counter = Counter()
		for route in self.routes:
			counter.update(route)
		duplicates = {i:j for i,j in counter.iteritems() if j > 1}
		incrementor = {i:0 for i,j in duplicates.iteritems()}

		# create new graph by duplicating edges that appear a few times
		transitNetwork = nx.Graph()
		for route in self.routes:
			for a, b in self.get_edges(route):
				e1, e2 = str(a), str(b)
				if a in incrementor:
					e1 = self._generate_name(e1, incrementor[a])
				if b in incrementor:
					e2 = self._generate_name(e2, incrementor[b])
				transitNetwork.add_edge(e1, e2, weight = self.transportNetwork.edge[a][b]['weight'])
			for r in route:
				if r in incrementor:
					incrementor[r] += 1

		# create transit edges between all edges of similar suffix
		for node, appearances in duplicates.iteritems():
			split_nodes = self._generate_names(str(node), appearances)
			for a, b in itertools.combinations(split_nodes, 2):
				transitNetwork.add_edge(a, b, weight = consts.transfer_penalty)

		# run all pairs shortest path algorithm
		all_pairs = nx.algorithms.all_pairs_shortest_path_length(transitNetwork)

		# now calculate the sum of all the pairs for the minimum where we have transit edges
		total_sum = 0
		for source, dest in demand:
			a, b = str(source), str(dest)
			transfer_time = 0
			if source not in duplicates and dest not in duplicates:
				transfer_time = all_pairs[a][b]
			elif source not in duplicates and dest in duplicates:
				transfer_time = min(all_pairs[a][c] for c in self._generate_names(b, duplicates[dest]))
			elif source in duplicates and dest not in duplicates:
				transfer_time = min(all_pairs[c][b] for c in self._generate_names(a, duplicates[source]))
			else:
				split_nodes_a = self._generate_names(a, duplicates[source])
				split_nodes_b = self._generate_names(b, duplicates[dest])
				transfer_time = min(all_pairs[c][d] for c, d in itertools.product(split_nodes_a, split_nodes_b))
			total_sum += demand[(source,dest)] * transfer_time
		return total_sum

	def show(self):
		positions = nx.get_node_attributes(self.transportNetwork, 'pos')
		nx.draw(self.transportNetwork, positions, node_size = 300)
		labels = {n:n for n in self.transportNetwork.nodes()}
		nx.draw_networkx_labels(self.transportNetwork, positions, labels=labels)
		for i in range(len(self.routes)):
			nx.draw_networkx_edges(self.transportNetwork, positions, edgelist = self.get_edges(self.routes[i]), alpha = 0.2, edge_color = consts.COLORS[i], width = 8)
		plt.show()