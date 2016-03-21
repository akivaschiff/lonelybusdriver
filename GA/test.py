from __future__ import print_function
import networkx as nx
from Routeset import Routeset
import MapLoader
import consts
from GenerateRouteset import repair
from GenerateRouteset import generateRouteset
from Generation import *
import random
import time
import sys

def generate_initial_population(transportNetwork, population_size):
	''' return an initial population of the requested size with costs '''
	population = []
	tries = 0
	cur_time = time.time()
	while len(population) < population_size:
		if time.time() - cur_time > 3:
			print("running 3 seconds... generated %d individuals of %d" % (len(population), tries))
			cur_time = time.time()
		completed, individual = generateRouteset(transportNetwork, consts.num_routes, consts.max_route_len, consts.min_route_len)
		tries += 1
		if completed:
			individual.calc_scores()
			population.append(individual)
	return population

def get_another_parent_index(number, range):
	parent2_index = random.randint(0,range)
	#parent2 = random.choice(population)
	while number == parent2_index:
		parent2_index = random.randint(0,range)
	return parent2_index

def SEAMO2(transportNetwork, population_size, generation_count):
	population = generate_initial_population(transportNetwork, population_size)
	objectives = ["passengers", "operator"]
	best_objective = {obj_name: min(population, key = lambda x: x.scores[obj_name]) for obj_name in objectives}
	#print [best_objective[key].get_scores() for key in objectives]
	for generation in range(generation_count):
		print("new generation")
		print(best_objective)
		for parent1_index in range(population_size):
			# select parent 1
			parent1 = population[parent1_index]
			# select parent 2
			parent2_index = random.randint(0, population_size - 1)
			parent2 = population[parent2_index]
			# generate an offspring
			offspring = crossover(parent1, parent2, transportNetwork)
			if not offspring:
				continue

			# repair the offspring - this shouldn't be necessary
			repair(offspring, transportNetwork, max_len = consts.max_route_len, min_len = consts.min_route_len)

			# apply mutation - gamma ray radiation
			mutate(offspring, consts.num_routes, consts.max_route_len, consts.min_route_len)
			if len(offspring.covered) < len(offspring.transportNetwork.nodes()):
				continue
			# this is a heavy function
			offspring.calc_scores()

			# insert offspring into population
			if offspring in population:
				continue
			# if offspring dominates either parent
			elif offspring.dominates(parent1):
				#print "offspring dominates parent 1"
				population[parent1_index] = offspring
			elif offspring.dominates(parent2):
				#print "offspring dominates parent 2"
				population[parent2_index] = offspring
			# if offspring dominates best so far objective
			elif offspring.get_scores()["passengers"] < best_objective["passengers"].get_scores()["passengers"]:
				best_objective["passengers"] = offspring
				if not parent1 == best_objective["operator"]:
					population[parent1_index] = offspring
				elif not parent2 == best_objective["operator"]:
					population[parent2_index] = offspring
			elif offspring.get_scores()["operator"] < best_objective["operator"].get_scores()["operator"]:
				best_objective["operator"] = offspring
				if not parent1 == best_objective["passengers"]:
					population[parent1_index] = offspring
				elif not parent2 == best_objective["passengers"]:
					population[parent2_index] = offspring
			# mutual non dominatoion
			elif not parent1.dominates(offspring) and not parent2.dominates(offspring):
				for ind in range(population_size):
					if offspring.dominates(population[ind]):
						population[ind] = offspring
						break
			# just delete offspring
			else:
				continue

'''
The following code demonstrates mutation
'''
transportNetwork = MapLoader.parse_map("Mandl")
population = generate_initial_population(transportNetwork, 1)[0]
population.save()
mutate(population, consts.num_routes, consts.max_route_len, consts.min_route_len)
population.save()
sys.exit(0)

'''
The following code demonstrates a crossover
'''
transportNetwork = MapLoader.parse_map("Mandl")
parent1, parent2 = generate_initial_population(transportNetwork, 2)
offspring = crossover(parent1, parent2, transportNetwork)
offspring.save()
parent1.imagecounter = 101
parent1.save()
parent2.imagecounter = 102
parent2.save()
sys.exit(0)

'''
The following code is for generating images of a solution-generation
'''
transportNetwork = MapLoader.parse_map("Mandl")
population = generate_initial_population(transportNetwork, 1)[0]
rs = Routeset(consts.num_routes, transportNetwork)
for route_num, stop in population.stops_and_route_nums:
	if stop == 'reverse':
		rs.reverse(route_num)
	else:
		rs.add_stop(route_num, stop, True)
rs.show()
sys.exit(0)



# 3,4,5
SEAMO2(transportNetwork, 100, 100)
sys.exit(0)


# try:
# 	child.get_passenger_cost(demand)
# except:
# 	print "exception"



