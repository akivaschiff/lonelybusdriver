import networkx as nx
import matplotlib.pyplot as plt
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
	def calc_route_length(self, route):
		return sum([self.transportNetwork.edge[route[j]][route[j+1]]['weight'] for j in range(len(route)-1)])
	def get_operator_cost(self):
		return sum([self.calc_route_length(route) for route in self.routes])
	def get_edges(self, route):
		return [(route[j],route[j+1]) for j in range(len(route)-1)]
	def get_passenger_cost(self):
		# construct new graph
		# run all pairs shortest path algorithm
		pass
	def is_feasable(self):
		pass

	def show(self):
		positions = nx.get_node_attributes(self.transportNetwork, 'pos')
		nx.draw(self.transportNetwork, positions, node_size = 300)
		labels = {n:n for n in self.transportNetwork.nodes()}
		nx.draw_networkx_labels(self.transportNetwork, positions, labels=labels)
		for i in range(len(self.routes)):
			nx.draw_networkx_edges(self.transportNetwork, positions, edgelist = self.get_edges(self.routes[i]), alpha = 0.3, edge_color = consts.COLORS[i], width = 8)
		plt.show()