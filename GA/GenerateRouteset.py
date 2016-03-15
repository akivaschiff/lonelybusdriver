import random

def generateRouteset(cityMap, num_routes, max_len, min_len):
	chosen = []
	routeset = Routeset(num_routes)
	for routes in range(num_routes):
		route_len = randint(min_len, max_len)
		if routes == 1:
			added_node = random.choice(cityMap.g.nodes)
		else:
			added_node = random.choice(chosen)
		routeset.add_stop(route, added_node)
		chosen.append(added_node)
		current_len = 1
		reverses = 0
		while (current_len <= route_len) and (reverses < 2):
		unused = [node for node in cityMap.get_neighbors(added_node) if node not in routeset[route]]
		if unused:
			added_node = random.choice(unused)
			routeset.add_stop(route, added_node)
			chosen.append(added_node)
			current_len += 1
		else:
			routeset.reverse(route)
			reverses += 1

	if len(chosen) < len(cityMap):
		if routeset.repair(chosen, len(cityMap), num_routes, max_len, min_len):
			return routeset
	return []