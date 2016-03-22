from Routeset import Routeset
from GenerateRouteset import generateRouteset
import itertools
import random
import time

def crossover(parent1, parent2, transportNetwork, problem):
	'''
	Attempt to crossover two parents and create an offspring
	Warning: offspring may need repairing - do not assume it covers entire graph
	'''
	offspring = Routeset(problem.busses, transportNetwork)
	# switch between parents and records the paths already chosen
	switch_parent = itertools.cycle([(parent1, set()), (parent2, set())])
	current_parent, paths_chosen = next(switch_parent)
	seed_index = random.randint(0, len(parent1.get_routes()) - 1)
	seed_route = parent1.get_route(seed_index)
	paths_chosen.add(seed_index)
	# add seed path to offspring
	offspring.add_route(seed_route, 0)
	for route_num in range(1, len(offspring.routes)):
		# switch to the next parent
		current_parent, paths_chosen = next(switch_parent)
		best_route_index = choose_route(current_parent, paths_chosen, offspring)
		offspring.add_route(current_parent.get_route(best_route_index), route_num)
		paths_chosen.add(best_route_index)
	return offspring

def mutate(routeset, num_routes, max_len, min_len):
	'''
	Mutate a given Routeset either by adding or deleting stops
	Note: If gets a legal solution - mutated solution will also be legal
	'''
	num_nodes_to_change = random.randint(1, num_routes*(max_len/2))
	mut = random.choice([add_nodes,delete_nodes])
	return mut(routeset, num_routes, num_nodes_to_change, max_len, min_len)


def generate_initial_population(transportNetwork, problem):
    '''
    Return an initial population of the requested size
    '''
    population = []
    cur_time = time.time()
    while len(population) < problem.initial:
        if time.time() - cur_time > 3:
            print "running 3 seconds... generated %d individuals of problem.initial" % (len(population))
            cur_time = time.time()
        completed, individual = generateRouteset(transportNetwork, problem.busses, problem.max, problem.min)
        if completed:
            individual.calc_scores()
            population.append(individual)
    print 'Finished generating initial population!'
    return population

def choose_route(parent, paths_chosen, offspring):
	'''
	Helper function for crossover - helps select a route to take from the parent to pass on to the offspring
	'''
	best_value = 0
	best_index = 0
	if len(offspring.covered) == len(parent.covered):
		# all nodes are covered - we just want a random unchosen path
		best_index = random.sample(set(range(0, len(parent.routes))).difference(paths_chosen), 1)[0]
		return best_index
	for i, route in enumerate(parent.get_routes()):
		if i in paths_chosen:
			continue
		# calculate the intersection of the route with the visited nodes of the offspring
		intersection = set(route).intersection(offspring.covered)
		# if there is no intersection - just carry on
		if len(intersection) == 0:
			continue
		#compute value for each route (percetage of new nodes in route)
		value = (len(route) - len(intersection)) / float(len(route))
		if value > best_value:
			best_value, best_index = value, i
		elif value == best_value:
			best_index = random.choice([i, best_index])

	return best_index

def add_nodes(routeset, num_routes, num_nodes_to_add, max_len, min_len):
	'''
	A type of mutation - attempts to add num_nodes_to_add to the routeset
	'''
	#constraints: route doesn't pass max_len, no return to same node twice in route
	added_nodes = 0
	tried = set()
	while (added_nodes < num_nodes_to_add) and (len(tried) < num_routes):
		# select a route to expand
		routes_to_expand = [(i,r) for i,r in enumerate(routeset.routes) if len(r) < max_len and i not in tried]
		if not routes_to_expand:
			return
		route_num, route = random.choice(routes_to_expand)

		# try adding nodes to either end until reached max_len
		while (len(routeset.get_route(route_num)) < max_len) and (len(tried) < num_routes):
			to_add = [node for node in routeset.transportNetwork.neighbors(routeset.get_last_stop(route_num)) if not routeset.contains(route_num, node)]
			if not to_add:
				routeset.reverse(route_num)
				to_add = [node for node in routeset.transportNetwork.neighbors(routeset.get_last_stop(route_num)) if not routeset.contains(route_num, node)]
			if to_add:
				selected = random.choice(to_add)
				routeset.add_stop(route_num, selected)
				added_nodes += 1
			else:
				# didn't manage to add any to this route - give up on it
				tried.add(route_num)
				break

def delete_nodes(routeset, num_routes, num_nodes_to_delete, max_len, min_len):
	'''
	A type of mutation - attempts to remove num_nodes_to_delete stops from the routeset
	'''
	#constraints: route doesn't pass min_len, graph still connected and covered
	deleted_nodes = 0
	tried = set()
	while (deleted_nodes < num_nodes_to_delete) and (len(tried) < num_routes):
		# select a route to trim
		routes_to_trim = [(i,r) for i,r in enumerate(routeset.routes) if len(r) > min_len and i not in tried]
		if not routes_to_trim:
			return
		route_num, route = random.choice(routes_to_trim)

		# try deleting nodes from either end until reached min_len
		other_nodes = set([node for i, route in enumerate(routeset.get_routes()) if i != route_num for node in route])
		while len(routeset.get_route(route_num)) > min_len:
			succeeded = routeset.try_remove_last_stop(route_num)
			if not succeeded:
				routeset.reverse(route_num)
				succeeded_reverse = routeset.try_remove_last_stop(route_num)
				if not succeeded_reverse:
					# didn't manage to trim this route - give up on it
					tried.add(route_num)
					break
			deleted_nodes += 1