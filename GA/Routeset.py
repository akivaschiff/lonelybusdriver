import random

class Routeset(object):
	def __init__(self, num_routes):
		self.routes = [[] for _ in range(num_routes)]
	def add_stop(route_num, node):
		self.routes[route_num].append(node)
	def reverse(route_num):
		self.routes[route_num].reverse()
