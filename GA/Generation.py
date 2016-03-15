import Routeset
import GenerateRouteset
import random
import itertools

def crossover(parent1, parent2, num_routes, transportNetwork):
	offspring = Routeset(num_routes, transportNetwork)
	switch_parent = itertools.cycle([parent2, parent1])
	offspring.add_route(random.choice(parent1.get_routes()))
	current_parent = next(switch_parent)
	for route in range(num_routes - 1):
		new_route = choose_route(current_parent, offspring)
		offspring.add_route(new_route)
		current_parent = next(switch_parent)
	return offspring
		
def choose_route(parent, offspring):
	#create a set of all visited nodes so far in offspring
	visited_nodes = set([node for route in offspring.get_routes for node in route])
	#choose among parent's routes only those that intersect with visited nodes
	possible_new_routes = [route for route in parent.get_routes() if set(route).intersection(visited_nodes)]
	#compute value for each route (percetage of new nodes in route)
	routes_value = [len(set(route).difference(visited_nodes))/len(route) for route in possible_new_routes]
	#return best route
	return possible_new_routes.index(max(routes_value))
	
def mutation(routeset, num_routes, max_len):
	num_nodes_to_change = random.randint(1, num_routes*(max_len/2))
	mut = random.choice([add_nodes,delete_nodes])
	return mut(routeset, num_nodes_to_change)
	
def add_nodes(routeset, num_nodes_to_change):
	pass
	
def delete_nodes(routeset, num_nodes_to_change):
	pass
	
	