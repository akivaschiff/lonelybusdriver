import networkx as nx
from Routeset import Routeset
import MapLoader
import consts
from GenerateRouteset import repair
from GenerateRouteset import generateRouteset
from Generation import crossover
import sys

#g, demand = MapLoader.parse_map("Mumford0")
g, demand = MapLoader.parse_map("Mandl")
dij_sum = float(sum(demand.values()))
# sys.exit(0)

population = []
for i in range(100):
	individual = generateRouteset(g, consts.num_routes, consts.max_route_len, consts.min_route_len)
	if individual:
		individual.calc_scores(demand, dij_sum)
		population.append(individual)
print len(population)
population[-1].show()
sys.exit(0)


print child.get_passenger_cost(demand)
for route in child.routes:
	print route
child.show()

# try:
# 	child.get_passenger_cost(demand)
# except:
# 	print "exception"



