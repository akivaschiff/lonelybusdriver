import random
from Routeset import Routeset

def generateRouteset(transportNetwork, num_routes, max_len, min_len):
	chosen = set()
	routeset = Routeset(num_routes, transportNetwork)
	for route_num in range(num_routes):
		route_len = random.randint(min_len, max_len)
		if route_num == 0:
			added_node = random.choice(transportNetwork.nodes())
		else:
			added_node = random.sample(chosen,1)[0]
		routeset.add_stop(route_num, added_node)
		chosen.add(added_node)
		current_len = 1
		reverses = 0
		while (current_len <= route_len) and (reverses < 2):
			unused = [node for node in transportNetwork.neighbors(added_node) if node not in routeset.routes[route_num]]
			if unused:
				added_node = random.sample(unused,1)[0]
				routeset.add_stop(route_num, added_node)
				chosen.add(added_node)
				current_len += 1
			else:
				routeset.reverse(route_num)
				reverses += 1

	n = len(transportNetwork.nodes())
	if len(chosen) < n:
		if routeset.repair(chosen, n, num_routes, max_len, min_len):
			return routeset
	return []