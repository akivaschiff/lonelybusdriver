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
	def repair(self, chosen, n, num_routes, max_len, min_len):
		tried = []
		while len(chosen) < n:
			# select a route to expand
			routes_to_expand = [(i,r) for i,r in enumerate(self.routes) if len(r) < max_len and i not in tried]
			if not routes_to_expand:
				return False
			index, route = random.choice(routes_to_expand)

			print route, chosen
			print tried
			# try adding a node to either end
			to_add = [node for node in self.transportNetwork.neighbors(self.routes[index][-1]) if node not in chosen and node not in route]
			selected = None
			if to_add:
				selected = random.choice(to_add)
			else:
				self.reverse(index)
				to_add_back = [node for node in self.transportNetwork.neighbors(self.routes[index][-1]) if node not in chosen and node not in route]
				if to_add_back:
					selected = random.choice(to_add_back)
			if selected:
				self.add_stop(index, selected)
				chosen.add(selected)
			else:
				# didn't manage to add any to this route - give up on it
				tried.append(i)
		return True

	def show(self):
		positions = nx.get_node_attributes(self.transportNetwork, 'pos')
		nx.draw(self.transportNetwork, positions, node_size = 300)
		labels = {n:n for n in self.transportNetwork.nodes()}
		nx.draw_networkx_labels(self.transportNetwork, positions, labels=labels)
		for i in range(len(self.routes)):
			nx.draw_networkx_edges(self.transportNetwork, positions, edgelist = self.get_edges(self.routes[i]), alpha = 0.3, edge_color = consts.COLORS[i], width = 8)
		plt.show()