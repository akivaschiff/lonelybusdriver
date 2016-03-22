
import networkx
import math
import json 


class CityMap:

    COLORS = ['r', 'g', 'b', 'y', 'orange']
    
    def __init__(self, map_file=None, map_json=None):
        """
        @param map_file, location to the city map file.
        """
        if map_file:
            with open(map_file, "r") as temp_map:
                self.map_file = json.load(temp_map)
        self.g = networkx.Graph()
        self._read_nodes()
        self._read_edges()
        self.number_of_busses = self.map_file["lines"]
        self.routes = {i: [] for i in range(1, self.number_of_busses + 1)}
        self.passengers = self.map_file["passengers"]
        self.map_weight = self.get_total_weight()
        self._calculate_nodes_size()
        self._build_nodes_colors()
        self.rv = set()
        for s, d in self.passengers:
            self.rv.add(s)
            self.rv.add(d)

    def _build_nodes_colors(self):
        self.nodes_colors = {v: 'grey' for v in self.g.nodes()}
        for s, d in self.passengers:
            if self.nodes_colors[s] == "grey" or self.nodes_colors[s] == "red":
                self.nodes_colors[s] = 'red'
            else:
                self.nodes_colors[s] = 'purple'

            if self.nodes_colors[d] == "grey" or self.nodes_colors[s] == "blue":
                self.nodes_colors[d] = 'blue'
            else:
                self.nodes_colors[d] = "purple"

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
        self.minx = min([self.pos[v][0] for v in self.pos])
        self.maxx = max([self.pos[v][0] for v in self.pos])
        self.miny = min([self.pos[v][1] for v in self.pos])
        self.maxy = max([self.pos[v][1] for v in self.pos])
            
    def _read_edges(self):
        self.edges_labels = {}
        for road in self.map_file["roads"]:
            self.g.add_edge(*road, weight=self.get_weight(road))
            self.edges_labels[tuple(road)] = int(self.get_weight(road))

    def update(self):
        to_remove = [e for e in self.edges_labels if e not in self.g.edges()]
        for e in to_remove:
            self.edges_labels.pop(e)

        to_remove = [v for v in self.labels if v not in self.g.nodes()]
        for v in to_remove:
            self.labels.pop(v)

    def _build_edge_list(self, line_number):
        edge_list = []
        for i in range(len(self.routes[line_number])-1):
            edge_list.append((self.routes[line_number][i], self.routes[line_number][i+1]))
        return edge_list
    

    def node_clusters(self, cluster_object):
        # map node -> cluster
        self.cluster_colors = {i+1: CityMap.COLORS[i+1] for i, c in enumerate(cluster_object)}
        self.cluster_colors[0] = "grey"
        self.clusters = {v: 0 for v in self.g.nodes()}
        tmp = {p.name: i+1 for i, c in enumerate(cluster_object) for p in c.points}
        for v in self.rv:
            self.clusters[v] = tmp[v]


    def draw(self):
        networkx.draw_networkx_nodes(self.g, self.pos,
                                     node_size=[300 + 300*self.nodes_size[v] for v in self.g.nodes()],
                                     node_color=[self.nodes_colors[v] for v in self.g.nodes()])
        networkx.draw_networkx_edges(self.g, self.pos)
        networkx.draw_networkx_labels(self.g, self.pos, labels=self.labels)
        networkx.draw_networkx_edge_labels(self.g, self.pos, edge_labels=self.edges_labels)
        for route in self.routes:
            if not self.routes[route]:
                continue
            edge_list = self._build_edge_list(route)
            networkx.draw_networkx_edges(self.g, self.pos, edge_color=CityMap.COLORS[route-1],
                                         width=2.0, edgelist=edge_list)


    def draw_clusters(self):
        networkx.draw_networkx_nodes(self.g, self.pos,
                                     node_size=[300 + 300*self.nodes_size[v] for v in self.g.nodes()],
                                     node_color=[self.cluster_colors[self.clusters[v]] for v in self.g.nodes()])
        networkx.draw_networkx_edges(self.g, self.pos)
        networkx.draw_networkx_labels(self.g, self.pos, labels=self.labels)
        networkx.draw_networkx_edge_labels(self.g, self.pos, edge_labels=self.edges_labels)
        for route in self.routes:
            if not self.routes[route]:
                continue
            edge_list = self._build_edge_list(route)
            networkx.draw_networkx_edges(self.g, self.pos, edge_color=CityMap.COLORS[route-1],
                                         width=2.0, edgelist=edge_list)

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

    def get_route_weight_from_route(self, route):
        edge_list = [(route[i], route[i+1]) for i in range(len(route)-1)]
        return sum([self.get_weight(edge) for edge in edge_list])
    
    def euclid_distance_by_name(self, pos1, pos2):
        P1 = self.pos[pos1]
        P2 = self.pos[pos2]
        return CityMap.euclid_distance(P1, P2)

    def get_total_cost(self):
        edges = set()
        for route in self.routes:
            for i in range(len(self.routes[route])-1):
                edges.add((self.routes[route][i], self.routes[route][i+1]))

        return sum([self.get_weight(e) for e in edges])

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

