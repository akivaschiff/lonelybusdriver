
import networkx
import math
import json 


class CityMap:

    COLORS = ['r', 'g', 'b', 'y', 'o']
    
    def __init__(self, map_file):
        """
        @param map_file, location to the city map file.
        """
        self.g = networkx.Graph()
        with open(map_file, "r") as temp_map:
            self.map_file = json.load(temp_map)
        self._read_nodes()
        self._read_edges()
        self.number_of_busses = self.map_file["lines"]
        self.routes = {i: [] for i in range(1, self.number_of_busses + 1)}
        self.passengers = self.map_file["passengers"]
        self.map_weight = self.get_total_weight()
        self._calculate_nodes_size()

    def _calculate_nodes_size(self):
        self.nodes_size = {v: 0 for v in self.g.nodes()}
        for s, d in self.passengers:
            self.nodes_size[s] += 1

    def _read_nodes(self):
        self.labels = {}
        self.pos = {}
        for name, x, y in self.map_file["stations"]:
            self.g.add_node(name)
            self.labels[name] = name
            self.pos[name] = (x, y)
            
    def _read_edges(self):
        self.edges_labels = {}
        for road in self.map_file["roads"]:
            self.g.add_edge(*road)
            self.edges_labels[tuple(road)] = int(self.get_weight(road))
            
    def _build_edge_list(self, line_number):
        edge_list = []
        for i in range(len(self.routes[line_number])-1):
            edge_list.append((self.routes[line_number][i], self.routes[line_number][i+1]))
        return edge_list
    
    def draw(self):
        networkx.draw_networkx_nodes(self.g, self.pos,
                                     node_size=[300 + 300*self.nodes_size[v] for v in self.g.nodes()],
                                     node_color=["red" if self.nodes_size[v] else "grey" for v in self.g.nodes()])
        networkx.draw_networkx_edges(self.g, self.pos)
        networkx.draw_networkx_labels(self.g, self.pos, labels=self.labels)
        networkx.draw_networkx_edge_labels(self.g, self.pos, edge_labels=self.edges_labels)
        for route in self.routes:
            if not self.routes[route]:
                continue
            edge_list = self._build_edge_list(route)
            networkx.draw_networkx_edges(self.g, self.pos, edge_color=CityMap.COLORS[route-1], edgelist=edge_list)

    def get_weight(self, edge):
        return CityMap.euclid_distance(self.pos[edge[0]], self.pos[edge[1]])

    def get_total_weight(self):
        return sum([self.get_weight(edge) for edge in self.g.edges()])
    
    def get_neighbors(self, node):
        return self.g.neighbors(node)
        
    def __len__(self):
        return len(self.g.nodes())
    
    def set_route(self, line_number, route):
        self.routes[line_number] = route
        
    def get_route_weight(self, line_number):
        if not self.routes[line_number]:
            return 0
        edge_list = self._build_edge_list(line_number)
        x = [self.get_weight(edge) for edge in edge_list]
        return sum(x)
    
    def euclid_distance_by_name(self, pos1, pos2):
        P1 = self.pos[pos1]
        P2 = self.pos[pos2]
        return CityMap.euclid_distance(P1, P2)

    @staticmethod
    def euclid_distance(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
            


# In[122]:

#m = CityMap("map1.txt")
#m.set_route(1, ["name1", "name5", "name6"])
#m.draw()
#print m.get_route_weight(1)

