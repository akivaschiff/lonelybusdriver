import random
from Routeset import Routeset

def generateRouteset(transportNetwork, num_routes, max_len, min_len):
	# TODO: make sure routes are longer than some minimum
	chosen = set()
	routeset = Routeset(num_routes, transportNetwork)
	for route_num in range(num_routes):
		route_len = random.randint(min_len, max_len)
		print route_len, min_len,max_len
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
			print route_num, reverses, unused
			if unused:
				added_node = random.sample(unused,1)[0]
				routeset.add_stop(route_num, added_node)
				chosen.add(added_node)
				current_len += 1
			else:
				routeset.reverse(route_num)
				# select the last node in the newly reverse route
				added_node = routeset.get_last_stop(route_num)
				reverses += 1
	routeset.show()

	n = len(transportNetwork.nodes())
	if len(chosen) < n:
		if repair(routeset, chosen, transportNetwork, num_routes, max_len, min_len):
			return routeset
	return []

def repair(routeset, chosen, transportNetwork, num_routes, max_len, min_len):
	n = len(transportNetwork.nodes())
	tried = []
	while len(chosen) < n:
		# select a route to expand
		routes_to_expand = [(i,r) for i,r in enumerate(routeset.routes) if len(r) < max_len and i not in tried]
		if not routes_to_expand:
			return False
		index, route = random.choice(routes_to_expand)

		# try adding a node to either end
		to_add = [node for node in transportNetwork.neighbors(routeset.routes[index][-1]) if node not in chosen and node not in route]
		selected = None
		if to_add:
			selected = random.choice(to_add)
		else:
			routeset.reverse(index)
			to_add_back = [node for node in transportNetwork.neighbors(routeset.routes[index][-1]) if node not in chosen and node not in route]
			if to_add_back:
				selected = random.choice(to_add_back)
		if selected:
			routeset.add_stop(index, selected)
			chosen.add(selected)
		else:
			# didn't manage to add any to this route - give up on it
			tried.append(index)
	return True