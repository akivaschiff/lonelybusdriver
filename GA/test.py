import networkx as nx
from Routeset import Routeset
import MapLoader


g, demand = MapLoader.parse_map("Mandl")
routeset = Routeset(3, g)
routeset.routes = [[0,1,2,5,7,9,13],[8,14,6,9,12,10],[11,3,4,1,2]]
routeset.show()

