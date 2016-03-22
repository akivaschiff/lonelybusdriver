import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from math import sin, cos, atan
import itertools
import os
GEN_PATH = 'generating'

'''
The routeset class - This class represents a solution
'''

class Routeset(object):
	def __init__(self, transportNetwork, problem):
		# initiate the list of routes
		self.routes = [[] for _ in range(problem.busses)]
		# initiate helper 'set' of each route
		self._routes_set = [set() for _ in range(problem.busses)]
		# a map from all nodes to a set of routes they contain
		self._node_to_routes = {node: set() for node in transportNetwork.nodes()}
		# initiate graph to hold connectivity between routes
		self.routesNetwork = nx.Graph()
		[self.routesNetwork.add_node(i) for i in range(problem.busses)]
		# remember the covered nodes of all the bus routes
		self.covered = set()
		# save a pointer to the original graph
		self.transportNetwork = transportNetwork
		self.problem = problem
		self.scores = {}
		self.imagecounter = 0

	def add_stop(self, route_num, node, save = False):
		# add node to the list of routes and other datastructs
		if save:
			self.save()
		self.routes[route_num].append(node)
		self._routes_set[route_num].add(node)
		self.covered.add(node)

		# update the routesNetwork if more than one node connecting them - weight is number of connections
		for other_route in self._node_to_routes[node]:
			if other_route in self.routesNetwork.edge[route_num]:
				self.routesNetwork.edge[route_num][other_route]["weight"] += 1
			else:
				self.routesNetwork.add_edge(route_num, other_route, weight = 1)

		# update the node_to_route mapping with route through a node
		self._node_to_routes[node].add(route_num)

	def reverse(self, route_num):
		self.routes[route_num].reverse()
	def get_routes(self):
		return self.routes
	def get_route(self, route_num):
		return self.routes[route_num]
	def get_last_stop(self, route_num):
		return self.routes[route_num][-1]
	def contains(self, route_num, node):
		return node in self._routes_set[route_num]
	def add_route(self, route, route_num):
		# load a whole route to specific bus-number
		for node in route:
			self.add_stop(route_num, node)
	def delete_last_stop(self, route_num):
		# get the node to remove
		node = self.routes[route_num].pop(-1)
		self._routes_set[route_num].remove(node)
		# check if still covered and remove from node_to_route mapping:
		self._node_to_routes[node].remove(route_num)
		if len(self._node_to_routes[node]) == 0:
			self.covered.remove(node)

		# update the routesNetwork if they are not connected any more
		for other_route in self._node_to_routes[node]:
			self.routesNetwork.edge[route_num][other_route]["weight"] -= 1
			if self.routesNetwork.edge[route_num][other_route]["weight"] == 0:
				self.routesNetwork.remove_edge(route_num, other_route)

	def try_remove_last_stop(self, route_num):
		node = self.get_last_stop(route_num)
		# check if this is the only route through edge - we will destroy cover of graph
		if len(self._node_to_routes[node]) == 1:
			return False
		# verify connectivity
		self.delete_last_stop(route_num)
		if nx.algorithms.is_connected(self.routesNetwork):
			return True
		else:
			self.add_stop(route_num, node)
			return False

	def calc_route_length(self, route):
		return sum([self.transportNetwork.edge[route[j]][route[j+1]]['weight'] for j in range(len(route)-1)])
	def calc_operator_cost(self):
		return sum([self.calc_route_length(route) for route in self.routes])
	def calc_scores(self):
		self.scores['passengers'] = self.calc_passenger_cost()
		self.scores['operator'] = self.calc_operator_cost()
	def get_scores(self, key):
		return self.scores[key]
	def dominates(self, other):
		return all(self.scores[k] <= other.scores[k] for k in self.scores.keys())
	def get_edges(self, route):
		return [(route[j],route[j+1]) for j in range(len(route)-1)]
	def __eq__(self, other):
		# this is a little hacky but a fast way for comparing two solutions
		return all(self.scores[k] == other.scores[k] for k in self.scores.keys())
	def _generate_name(self, node, inc):
		return '%s_%s' % (node, chr(97 + inc))
	def _generate_names(self, node, number):
		return [self._generate_name(node, inc) for inc in range(number)]
	def __repr__(self):
		return "\n" + str(self.scores) + "\n" + "\n".join([str(r) for r in self.routes]) + '\n'
	def calc_passenger_cost(self):
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
				transitNetwork.add_edge(a, b, weight = self.problem.tf)

		# run all pairs shortest path algorithm
		all_pairs = nx.algorithms.floyd_warshall(transitNetwork, weight = "weight")

		# now calculate the sum of all the pairs for the minimum where we have transit edges
		total_sum = 0
		for source, dest in self.transportNetwork.demand:
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
			total_sum += self.transportNetwork.demand[(source,dest)] * transfer_time
		return total_sum / float(self.transportNetwork.dij_sum)

	def show(self, save = False):
		# count multi-edges
		counter = Counter()
		for route in self.routes:
			counter.update(self.get_edges(route))
			counter.update(self.get_edges(route[::-1]))
		duplicates = {i:j for i,j in counter.iteritems() if j > 1}
		incrementor = {i:0 for i,j in duplicates.iteritems()}

		# draw nodes
		positions = nx.get_node_attributes(self.transportNetwork, 'pos')
		nx.draw(self.transportNetwork, positions, node_size = 800, node_color = (1,0,1), edge_alpha = .3)
		labels = {n:n for n in self.transportNetwork.nodes()}
		nx.draw_networkx_labels(self.transportNetwork, positions, labels=labels)

		edges_labels = {edge:self.transportNetwork.get_edge_data(*edge)["weight"] for edge in self.transportNetwork.edges()}
		#nx.draw_networkx_edge_labels(self.transportNetwork, positions, edge_labels=edges_labels)

		for i in range(len(self.routes)):
			node_and_positions_original = nx.get_node_attributes(self.transportNetwork, 'pos')
			node_and_positions = nx.get_node_attributes(self.transportNetwork, 'pos')
			edges = self.get_edges(self.routes[i])
			for edge in edges:
				if edge not in duplicates:
					nx.draw_networkx_edges(self.transportNetwork, node_and_positions_original, \
					edgelist = [edge], alpha = 0.8, edge_color = self.problem.COLORS[i], \
					width = 6)
				if edge in duplicates:
					offset = (duplicates[edge] - incrementor[edge] - 1) * 0.09
					node1, node2 = edge
					x1, y1 = node_and_positions[node1]
					x2, y2 = node_and_positions[node2]
					angle = atan((y2 - y1) / (float(x2 - x1) + 0.0001))
					node_and_positions[node1] = (x1 - sin(angle) * offset, y1 + cos(angle) * offset)
					node_and_positions[node2] = (x2 - sin(angle) * offset, y2 + cos(angle) * offset)
					nx.draw_networkx_edges(self.transportNetwork, node_and_positions, \
					edgelist = [edge], alpha = 0.8, edge_color = self.problem.COLORS[i], \
					width = 6)
					node_and_positions[node1] = (x1, y1)
					node_and_positions[node1] = (x2, y2)
					incrementor[edge] += 1
					incrementor[edge[::-1]] += 1
			#nx.draw_networkx_edges(self.transportNetwork, node_and_positions, edgelist = self.get_edges(self.routes[i]), alpha = 0.5, edge_color = consts.COLORS[i], width = 8)
		if not save:
			plt.show()
		else:
			plt.savefig('%s%simage_%s.png' % (GEN_PATH, os.path.sep, str(self.imagecounter).zfill(3)), format = 'png')
			self.imagecounter += 1
		plt.clf()

	def save(self):
		self.show(True)
