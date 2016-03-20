import networkx
import CityMap
import matplotlib.pyplot as plt

def is_satisfied(city_map):
  """
  :param city_map: city map object
  :return: true iff all passeners can reach their goal.
  """
  for src, dst in city_map.passengers:
    if not networkx.has_path(city_map.g, src, dst):
      return False
  return True


def calculate_reduced_graph(city_map):
  #TODO: 1: What about several connected components?
  #TODO 2: run DFS to assign routes to lines

  # first calculate an MST
  mst = networkx.minimum_spanning_tree(city_map.g)
  sorted_edges = sorted(mst.edges(), key=lambda e: mst.get_edge_data(*e)['weight'], reverse=True)
  result = mst.copy()
  for e in sorted_edges:
    tmp_graph = result.copy()
    tmp_graph.remove_edge(*e)
    city_map.g = tmp_graph
    if is_satisfied(city_map):
      result = tmp_graph

  # remove all the irrelevant nodes (degree 0)
  nodes = result.nodes()
  for v in nodes:
    if not result.degree(v):
      result.remove_node(v)

  city_map.g = result
  city_map.update()
  return city_map



def main():
  g = CityMap.CityMap(r"maps\grid_14_1")
  calculate_reduced_graph(g)
  g.draw()
  plt.show()


if __name__ == "__main__":
  main()


