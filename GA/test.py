import networkx as nx
from Routeset import Routeset
import MapLoader
import consts
from GenerateRouteset import repair
from GenerateRouteset import generateRouteset
import sys

#g, demand = MapLoader.parse_map("Mumford0")
g, demand = MapLoader.parse_map("Mandl")
demand_norm = sum(demand.values())
# sys.exit(0)
# routeset.routes = [[0,1,2,5,7,9,13],[8,14,6,9,12,10],[11,3,4,1,2]]
routeset = Routeset(4, g)
routeset.routes = [[9,15], [1,2,4,5], [11,10,7,15,8,6,3,2], [14,13,11,12]]
routeset.show()
print routeset.get_operator_cost(), routeset.get_passenger_cost(demand) / float(demand_norm)
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



