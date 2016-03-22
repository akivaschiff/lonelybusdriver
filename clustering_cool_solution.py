import CityMap
import kmeans
import networkx
import matplotlib.pyplot as plt
import simple

class Problem:
  def __init__(self, graph):
    self.expanded = 0
    self.tmp_storage = {}
    self.graph = graph
    self.neighbors = {v: self.graph.neighbors(v) for v in self.graph.nodes()}

  def getStartState(self):
    return tuple()

  def isGoalState(self, state):
    return all([v in state for v in self.graph.nodes()])

  def getSuccessors(self, state):
  	self.expanded += 1
  	if state:
  		return [state + tuple([x]) for x in  self.neighbors[state[-1]]]
  	return [tuple([x]) for x in self.graph.nodes()]

  def getStateCost(self, state):
		# sum of all edges
    return sum([self.graph[state[i]][state[i+1]]['weight'] for i in range(len(state)-1)])


def floyd_warshall_solution_remove_stations(cityMap):
  nodes = cityMap.g.nodes()
  for v in nodes:
    if v not in cityMap.rv:
      cityMap.g.remove_node(v)

  all_short = networkx.floyd_warshall(cityMap.g)
  route = []
  for v in cityMap.g.nodes():
    route.append(min([node for node in all_short[v] if node not in route], key=lambda x: all_short[v][x]))

  routes = []
  segment = len(route) / cityMap.number_of_busses
  for i in range(segment):
		routes.append(route[i*segment: i*segment + segment])
		cityMap.set_route(i+1, route[i*segment: i*segment + segment])
		return routes


def clustering_map(cityMap, k):
	"""
	cluster the city map into k clusters.
	"""
	# convert all the cityMap vertices into k-means structure
	points = [kmeans.Point([cityMap.pos[v][0], cityMap.pos[v][1]], v) for v in cityMap.rv]

	# Cluster those data!
	opt_cutoff = 0.5
	clusters = kmeans.kmeans(points, k, opt_cutoff)
	cityMap.node_clusters(clusters)


def get_subgraph_center(cityMap, cluster_number):
	citycenter_x = (cityMap.minx + cityMap.maxx) / 2
	citycenter_y = (cityMap.miny + cityMap.maxy) / 2
	return min([v for v in cityMap.rv if cityMap.clusters[v] == cluster_number], 
		key=lambda v: CityMap.CityMap.euclid_distance((citycenter_x, citycenter_y), cityMap.pos[v]))


def hub_algo(c):
	all_short = networkx.all_pairs_dijkstra_path(c.g)

	clustering_map(c, c.number_of_busses-1)
	central_nodes = [get_subgraph_center(c, i) for i in range(1, c.number_of_busses)]

	central_route = []
	for i in range(len(central_nodes)-1):
		central_route += all_short[central_nodes[i]][central_nodes[i+1]]
	c.set_route(1, central_route)

	for i in range(1, len(central_nodes)+1):
		Gp =  networkx.Graph()
		for v in c.rv:
			for u in c.rv:
				if (v==u) or (c.clusters[u] != i) or (c.clusters[v] != i):
					continue
				Gp.add_edge(v, u, weight=c.get_route_weight_from_route(all_short[u][v]))

		problem = Problem(Gp)
		best = simple.aStarSearch(problem)

		new_route = []
		for j in range(len(best)-1):
			new_route += all_short[best[j]][best[j+1]]
		c.set_route(i + 1, new_route)
	return c


if __name__ == "__main__":
	c = CityMap.CityMap(r'maps\mundel.map')
	hub_algo(c)
	c.draw_clusters()
	plt.show()