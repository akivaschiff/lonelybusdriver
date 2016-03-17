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

def mutation(routeset, num_routes, max_len):
	num_nodes_to_change = random.randint(1, num_routes*(max_len/2))
	mut = random.choice([add_nodes,delete_nodes])
	return mut(routeset, num_nodes_to_change)

def add_nodes(routeset, num_nodes_to_change):
	pass

def delete_nodes(routeset, num_nodes_to_change):
	pass