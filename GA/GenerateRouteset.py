import random
from Routeset import Routeset

def generateRouteset(transportNetwork, problem):
	num_routes, max_len, min_len = problem.busses, problem.max, problem.min
	# TODO: make sure routes are longer than some minimum
	routeset = Routeset(transportNetwork, problem)
	for route_num in range(num_routes):
		route_len = random.randint(min_len, max_len)
		if route_num == 0:
			added_node = random.choice(transportNetwork.nodes())
		else:
			added_node = random.sample(routeset.covered,1)[0]
		routeset.add_stop(route_num, added_node)
		current_len = 1
		reverses = 0
		while (current_len <= route_len) and (reverses < 2):
			# choose the list of nodes we can add
			unused = [node for node in transportNetwork.neighbors(added_node) if not routeset.contains(route_num, node)]

			# check if there are any available
			if unused:
				added_node = random.sample(unused,1)[0]
				routeset.add_stop(route_num, added_node)
				current_len += 1
			else:
				routeset.reverse(route_num)
				# select the last node in the newly reverse route
				added_node = routeset.get_last_stop(route_num)
				reverses += 1

	# verify that we have covered all nodes - if not - we want to try and repair
	is_complete = True
	if len(routeset.covered) < len(transportNetwork.nodes()):
		is_complete = repair(routeset, transportNetwork, max_len, min_len)
	return is_complete, routeset

def repair(routeset, transportNetwork, max_len , min_len):
	tried = []
	while len(routeset.covered) < len(transportNetwork.nodes()):
		# select a route to expand
		routes_to_expand = [(i,r) for i,r in enumerate(routeset.routes) if len(r) < max_len and i not in tried]
		if not routes_to_expand:
			return False
		route_num, route = random.choice(routes_to_expand)

		# try adding a node to either end
		to_add = [node for node in transportNetwork.neighbors(routeset.get_last_stop(route_num)) if node not in routeset.covered and not routeset.contains(route_num, node)]
		if not to_add:
			# try again from the other side
			routeset.reverse(route_num)
			to_add = [node for node in transportNetwork.neighbors(routeset.get_last_stop(route_num)) if node not in routeset.covered and not routeset.contains(route_num, node)]
		if to_add:
			selected = random.choice(to_add)
			routeset.add_stop(route_num, selected)
		else:
			# didn't manage to add any to this route - give up on it
			tried.append(route_num)
	return True