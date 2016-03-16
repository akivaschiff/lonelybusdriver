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
demand_norm = sum(demand.values())
# sys.exit(0)
routeset1 = Routeset(4, g)
routeset2 = Routeset(4, g)
routeset1.routes = [[9,15],[1,2,4,5],[11,10,7,15,8,6,3,2],[14,13,11,12]]
routeset2.routes = [[1,2,3,6,8,10,11,13], [9,15,6,4,12,11,13,14], [14,10,7,15,6,4,2,1], [12,11,10,8,6,4,5,2]]
print routeset1.get_passenger_cost(demand), routeset1.get_operator_cost()
print routeset2.get_passenger_cost(demand), routeset2.get_operator_cost()
child = crossover(routeset1, routeset2, len(routeset1.routes), g)
print child.get_passenger_cost(demand), child.get_operator_cost()
sys.exit(0)

for i in range(500):
	child = generateRouteset(g, consts.num_routes, consts.max_route_len, consts.min_route_len)
	if child:
		print child.get_passenger_cost(demand)/demand_norm, child.get_operator_cost()
sys.exit(0)

print child.get_passenger_cost(demand)
for route in child.routes:
	print route
child.show()

# try:
# 	child.get_passenger_cost(demand)
# except:
# 	print "exception"



