import networkx


def total_destination_left_heuristic(state, problem):
  """
  CONSISTENT - admissible

  CONSISTENT if all vertices has same number of passengers

  :param state: the total amount of kilometers left between every passengers and his destination.
  :param problem: VRPProblem.
  :return: returns the sum of all the routes.
  """
  problem.tmp_storage.setdefault("minimal_edge", min([state.graph.get_weight(e) for e in state.graph.g.edges()]))

  total = [problem.tmp_storage["minimal_edge"] for p in state.passengers if not (p.onboard or p.is_arrived())]
  if not total:
    return 0
  return sum(total)


def distance_waiting_ratio(state, problem):
  """
  INCONSISTENT
  :param state:
  :param problem:
  :return: calculate the ratio between total_distance / waiting people
  """
  waiting = len([p for p in state.passengers if not (p.onboard or p.is_arrived())])
  if not waiting or (state.get_state_weight() == 0):
    return 0

  return float(waiting) / state.get_state_weight()

def satisfied_customers(state, problem):
  """
  CONSISTENT
  :param state:
  :param problem:
  :return: TOTAL_PASSENGERS - NUMBER_OF_SATISFIED_PASSENGERS
  """
  return len(problem.cityMap.passengers) - [p.is_arrived() for p in state.passengers].count(True)


def onboard_passengers(state, problem):
  """
  CONSISTENT
  :param state:
  :param problem:
  :return: TOTAL_PASSENGERS_UNSATISFIED - NUMBER_OF_ONBOARD_PASSENGERS
  """
  unsat = [p.is_arrived() for p in state.passengers].count(False)
  sat = len(state.passengers) - unsat
  onboard = [p for p in state.passengers if p.onboard]
  return unsat - (len(onboard) + sat)


def combined_total_destination_onboard(state, problem):
  """
  NOT CONSISTENT...
  :param state:
  :param problem:
  :return:
  """
  return onboard_passengers(state, problem) + total_destination_left_heuristic(state, problem)


import matplotlib.pyplot as plt

def get_subgraph(cityMap):
  all_relevant_nodes = set()
  all_short = networkx.floyd_warshall(cityMap.g)
  for s, d in cityMap.passengers:
    all_relevant_nodes.add(s)
    all_relevant_nodes.add(d)

  Gp =  networkx.Graph()
  for v in all_relevant_nodes:
    for u in all_relevant_nodes:
      if v==u:
        continue
      Gp.add_edge(v, u)

  cityMap.draw()
  plt.show()
  plt.clf()
  networkx.draw_networkx_nodes(Gp, cityMap.pos, node_color=[cityMap.nodes_colors[v] for v in Gp.nodes()])
  networkx.draw_networkx_edges(Gp, cityMap.pos)
  networkx.draw_networkx_labels(Gp, cityMap.pos, labels=cityMap.labels)
  networkx.draw_networkx_edge_labels(Gp, cityMap.pos, edge_labels={(u, v): str(all_short[u][v]) for u,v in Gp.edges()})
  plt.show()



def floyd_warshall_solution_remove_stations(cityMap):
  all_relevant_nodes = set()
  for s, d in cityMap.passengers:
    all_relevant_nodes.add(s)
    all_relevant_nodes.add(d)

  nodes = cityMap.g.nodes()
  for v in nodes:
    if v not in all_relevant_nodes:
      cityMap.g.remove_node(v)

  all_short = networkx.floyd_warshall(cityMap.g)
  route = []
  for v in cityMap.g.nodes():
    route.append(min([node for node in all_short[v] if node not in route], key=lambda x: all_short[v][x]))

  routes = []
  print route
  segment = len(route) / cityMap.number_of_busses
  for i in range(segment):
    routes.append(route[i*segment: i*segment + segment])
  return routes

if __name__ == "__main__":
  import CityMap
  get_subgraph(CityMap.CityMap(r'maps\grid_5_1'))