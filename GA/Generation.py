from Routeset import Routeset
import consts
import GenerateRouteset
import random
import itertools

def crossover(parent1, parent2, transportNetwork):
	offspring = Routeset(consts.num_routes, transportNetwork)
	switch_parent = itertools.cycle([parent2, parent1])
	seed_route = random.choice(parent1.get_routes())
	# keep a set of all nodes already visited by offspring
	visited_nodes = set(seed_route)
	offspring.routes[0] = seed_route
	current_parent = next(switch_parent)
	for r in range(1, consts.num_routes):
		new_route = choose_route(current_parent, visited_nodes)
		if new_route == []:
			print "NO ROUTE CHOSEN!!! THIS SHOULD NEVER HAPPEN!"
			return False
		visited_nodes.update(new_route)
		offspring.routes[r] = new_route
		current_parent = next(switch_parent)
	return offspring

def choose_route(parent, visited_nodes):
	best_value = 0
	best_route = []
	for i, route in enumerate(parent.get_routes()):
		# calculate the intersection of the route with the visited nodes of the offspring
		intersection = set(route).intersection(visited_nodes)
		# if there is no intersection - just carry on
		if len(intersection) == 0:
			continue
		#compute value for each route (percetage of new nodes in route)
		value = (len(route) - len(intersection)) / float(len(route))
		if value > best_value:
			best_value, best_route = value, route
		elif value == best_value:
			best_route = random.choice([route, best_route])

	return best_route

def mutation(routeset, num_routes, max_len, min_len):
	num_nodes_to_change = random.randint(1, num_routes*(max_len/2))
	mut = random.choice([add_nodes,delete_nodes])
	return mut(routeset, num_routes, num_nodes_to_change, max_len, min_len)

def add_nodes(routeset, num_routes, num_nodes_to_add, max_len, min_len):
	#constraints: route doesn't pass max_len, no return to same node twice in route
	added_nodes = 0
	tried = []
	while (added_nodes < num_nodes_to_add) and (len(tried) < num_routes):
		# select a route to expand
		routes_to_expand = [(i,r) for i,r in enumerate(routeset.routes) if len(r) < max_len and i not in tried]
		if not routes_to_expand:
			return False
		index, route = random.choice(routes_to_expand)

		# try adding nodes to either end until reached max_len
		while (len(routeset.get_route(index)) < max_len) and (len(tried) < num_routes):
			to_add = [node for node in routeset.transportNetwork.neighbors(routeset.get_last_stop(index)) if node not in route]
			selected = None
			if to_add:
				selected = random.choice(to_add)
			else:
				routeset.reverse(index)
				to_add_back = [node for node in routeset.transportNetwork.neighbors(routeset.get_last_stop(index)) if node not in route]
				if to_add_back:
					selected = random.choice(to_add_back)
			if selected is not None:
				routeset.add_stop(index, selected)
				added_nodes += 1
			else:
				# didn't manage to add any to this route - give up on it
				tried.append(index)
				break
	return True

def delete_nodes(routeset, num_routes, num_nodes_to_delete, max_len, min_len):
	#constraints: route doesn't pass min_len, graph still conected
	deleted_nodes = 0
	tried = []
	while (deleted_nodes < num_nodes_to_delete) and (len(tried) < num_routes):
		# select a route to trim
		routes_to_trim = [(i,r) for i,r in enumerate(routeset.routes) if len(r) > min_len and i not in tried]
		if not routes_to_trim:
			return False
		index, route = random.choice(routes_to_trim)

		# try deleting nodes from either end until reached min_len
		other_nodes = set([node for i, route in enumerate(routeset.get_routes()) if i != index for node in route])
		while len(routeset.get_route(index)) > min_len:
			to_delete = routeset.get_last_stop(index)
			# check minimal connectivity between other routes
			if len(set(routeset.get_route(index)).intersection(other_nodes)) == 1:
				tried.append(index)
				break
			# check connectivity of entire graph
			if to_delete not in other_nodes:
				routeset.reverse(index)
				to_delete = routeset.get_last_stop(index)
				if to_delete not in other_nodes:
					to_delete = None
			if to_delete is not None:
				routeset.delete_last_stop(index)
				deleted_nodes += 1
			else:
				# didn't manage to trim this route - give up on it
				tried.append(index)
				break
	return True
