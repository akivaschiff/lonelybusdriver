import networkx as nx
from Routeset import Routeset
import MapLoader
import consts
from GenerateRouteset import repair
from GenerateRouteset import generateRouteset
from Generation import crossover
import random
import time
import sys

def generate_initial_population(transportNetwork, population_size):
	''' return an initial population of the requested size with costs '''
	population = []
	cur_time = time.time()
	while len(population) < population_size:
		if time.time() - cur_time > 3:
			print "running 3 seconds... generated %d individuals" % len(population)
			cur_time = time.time()
		individual = generateRouteset(transportNetwork, consts.num_routes, consts.max_route_len, consts.min_route_len)
		if individual:
			individual.calc_scores()
			population.append(individual)
	return population

def select_another_parent(parent1, population):
	parent2 = random.choice(population)
	while parent2 == parent1:
		parent2 = random.choice(population)
	return parent2

def SEAMO2(transportNetwork, population_size, generation_count):
	population = generate_initial_population(transportNetwork, population_size)
	objectives = ["passengers", "operator"]
	best_objective = {obj_name: min(population, key = lambda x: x.scores[obj_name]) for obj_name in objectives}
	#print [best_objective[key].get_scores() for key in objectives]
	for counter in range(generation_count):
		for parent1 in population:
			# select parent 2
			parent2 = select_another_parent(parent1, population)
			# generate an offspring
			offspring = crossover(parent1, parent2, transportNetwork)


#g, demand = MapLoader.parse_map("Mumford0")
# sys.exit(0)
transportNetwork = MapLoader.parse_map("Mandl")
SEAMO2(transportNetwork, 20, 5)
sys.exit(0)


print child.calc_passenger_cost(demand)
for route in child.routes:
	print route
child.show()

# try:
# 	child.get_passenger_cost(demand)
# except:
# 	print "exception"



