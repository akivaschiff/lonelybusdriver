import sys
import copy
import time
import util
import pprint
import itertools
import problems
import CityMap
import matplotlib.pyplot as plt

class Passenger:
  """
  represent a passenger in our world. has source station, destination
  and boolean value - is arrived?
  """
  def __init__(self, source, dest):
    self.src = source
    self.dst = dest
    self.arrived = (source == dest)

  def set_arrived(self):
    self.arrived = True

  def is_arrived(self):
    return self.arrived


class Bus:
  def __init__(self, number):
    self.number = number
    self.route = []
    self.total_time = 0.0
    # this data structure is for quickly checking if an edge is in our route
    self.edges = set()

  def add_stop(self, node, weight):
    if weight:
      self.route.append(node)
      self.edges.add((self.route[-1], self.route[-2]))
      self.edges.add((self.route[-2], self.route[-1]))
      self.total_time += weight
    else:
      self.route.append(node)

  def build_edge_list(self):
    return [(self.route[i], self.route[i+1]) for i in range(len(self.route)-1)]

class RoutesState:
  def __init__(self, graph, numBusses, passengers):
    self.graph = graph
    self.busses = {}
    self.passengers = [Passenger(*p) for p in passengers]
    self.busses = {i: Bus(i) for i in range(numBusses)}

  def getShortestBus(self):
    return min(self.busses.values(), key = lambda x: x.total_time)

  def getCopy(self):
    newState = RoutesState(self.graph, len(self.busses), [])
    newState.busses = copy.deepcopy(self.busses)
    newState.passengers = copy.deepcopy(self.passengers)
    return newState

  def addStop(self, bus, stop, weight):
    self.busses[bus.number].add_stop(stop, weight)
    for p in self.passengers:
      if (stop == p.src) and (p.dst in self.busses[bus.number].route):
        p.set_arrived()

  def get_route_weight(self, line_number):
    if not self.busses[line_number]:
        return 0
    edge_list = self.busses[line_number].build_edge_list()
    x = [self.graph.get_weight(edge) for edge in edge_list]
    return sum(x)

  def get_state_weight(self):
    """
    calculate the entire state.
    """
    return sum([self.get_route_weight(line) for line in self.busses])

  def __hash__(self):
    return hash(self.busses[i].edges)

  def __repr__(self):
    return "\n".join([str(b.number) + ': ' + str(b.route) for b in self.busses.values()])

def breadthFirstSearch(problem, return_all = False):
  "Search the shallowest nodes in the search tree first. [p 81]"
  problem.expanded = 0
  nodes = util.Queue()
  nodes.push(problem.getStartState())
  seen = set([])
  all_solutions = []

  while not nodes.isEmpty():
    problem.expanded += 1
    current_node = nodes.pop()
    # if we've already reached this point in the graph before - move on
    if current_node in seen:
        continue
    seen.add(current_node)
    if problem.isGoalState(current_node):
        # we found the goal!
        if return_all:
          all_solutions.append(current_node)
          continue
        else:
          #print "found goal!", current_node.get_state_weight(), current_node
          return current_node
    new_states = problem.getSuccessors(current_node)
    new_states = [s for s in new_states if s not in seen]
    for state in new_states:
        nodes.push(state)

  return all_solutions # this will be empty if return_all flag was false

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  problem.expanded = 0
  nodes = util.PriorityQueue()
  nodes.push(problem.getStartState(), 0)

  seen = []
  while not nodes.isEmpty():
    current_node = nodes.pop()
    problem.expanded += 1
    if current_node in seen:
        continue

    seen.append(current_node)
    if problem.isGoalState(current_node):
        print current_node.get_state_weight()
        #goalStates.add(current_node.get_state_weight())
        return current_node

    new_states = problem.getSuccessors(current_node)
    new_states = [s for s in new_states if s not in seen]

    for state in new_states:
      cost = state.get_state_weight()
      new_cost = cost + heuristic(state, problem)
      nodes.push(state, new_cost)

  return []


def test(alg, initState):
  start_time = time.time()
  if alg == 'bfs':
    prob = problems.WeightedProblem(initState)
    final_route = breadthFirstSearch(prob)
  elif alg == 'astar':
    prob = problems.WeightedProblem(initState)
    final_route = aStarSearch(prob)
  else:
    print 'unknown algorithm'
    return

  end_time = time.time() - start_time
  print "==============================================="
  if not final_route:
    print "NO SOLUTION!"
    return 0
  else:
    print "SOLUTION:"
    pprint.pprint(final_route)

  print 'NODES EXPANDED: %d' % (prob.expanded)
  print 'TIME: %d' % (end_time)
  print "==============================================="
  for busnum, bus in final_route.busses.iteritems():
    initState.graph.set_route(busnum+1, bus.route)
  return (end_time, final_route.get_state_weight(), prob.expanded)

def run_simple_test(alg):
  NUMBER_OF_TESTS = 10
  result = {}
  for i in range(5, 6):
    graph = CityMap.CityMap(r"maps\mesh_%d_%d" % (i, 1))
    print r"maps\mesh_%d_%d" % (i, 1)
    initState = RoutesState(graph, graph.number_of_busses, graph.passengers)
    result[i] = test(alg, initState)
    graph.draw()
    plt.show()
  return result


def main(alg = 'bfs'):
  #graph = CityMap.CityMap("maps\\5ring3bus.txt")
  print run_simple_test(alg)


if __name__ == '__main__':
  alg_name = sys.argv[1]
  main(alg_name)
