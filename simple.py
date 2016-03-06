import sys
import copy
import time
import util
import pprint
import itertools
import problems
import CityMap
import matplotlib.pyplot as plt

EXPANDED_NODES = 0

class Bus:
  def __init__(self, number, final_stop):
    self.number = number
    self.route = [final_stop]
    self.final_stop = final_stop
    self.total_time = 0.0
  def add_stop(self, node, weight):
    self.route.append(node)
    self.total_time += weight

class RoutesState:
  def __init__(self, graph, numBusses, finalStop):
    self.graph = graph
    self.busses = {}
    self.finalStop = finalStop
    self.covered = set()
    self.covered.add(finalStop)
    for i in range(numBusses):
      self.busses[i] = Bus(i,finalStop)
  def getShortestBus(self):
    return min(self.busses.values(), key = lambda x: x.total_time)
  def getCopy(self):
    newState = RoutesState(self.graph, len(self.busses), self.finalStop)
    newState.covered = set(self.covered)
    newState.busses = copy.deepcopy(self.busses)
    return newState
  def addStop(self, bus, stop, weight):
    self.busses[bus.number].add_stop(stop, weight)
    self.covered.add(stop)
  def __hash__(self):
    return hash(tuple([tuple(bus.routes) for bus in self.busses.values()]))
  def __repr__(self):
    return "\n".join([str(b.number) + ': ' + str(b.route) for b in self.busses.values()]) + \
           '\n>> Covered: ' + str(self.covered)


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  global EXPANDED_NODES
  nodes = util.Queue()
  nodes.push(problem.getStartState())
  seen = []

  while not nodes.isEmpty():
    EXPANDED_NODES += 1
    current_node = nodes.pop()
    # if we've already reached this point in the graph before - move on
    if current_node in seen:
        continue
    seen.append(current_node)
    if problem.isGoalState(current_node):
        # we found the goal!
        return current_node
    new_states = problem.getSuccessors(current_node)
    new_states = [s for s in new_states if s not in seen]
    for state in new_states:
        nodes.push(state)

  return []

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  # PriorityQueue
  global EXPANDED_NODES
  nodes = util.PriorityQueue()
  nodes.push((problem.getStartState(),0),0)
  seen = []
  import pprint
  while not nodes.isEmpty():
    current_node, current_cost = nodes.pop()
    EXPANDED_NODES += 1
    #print('>>> current: %s, cost: %s, path: %s' % (str(current_node),current_cost,path))
    # if we've already reached this point in the graph before - move on
    if current_node in seen:
        continue
    seen.append(current_node)
    if problem.isGoalState(current_node):
        # we found the goal!
        return current_node
    new_states = problem.getSuccessors(current_node)
    new_states = [s for s in new_states if s[0] not in seen][::-1]
    for state, cost in new_states:
        new_cost = current_cost + cost + heuristic(state, problem)
        nodes.push((state,current_cost+cost),new_cost)

  return []

def cornersHeuristic(state, problem):
  pass


def main(alg = 'bfs'):
  #graph = CityMap.CityMap("maps\\5ring3bus.txt")
  graph = CityMap.CityMap("maps\\5mesh3bus.txt")
  initState = RoutesState(graph, graph.number_of_busses, graph.final_station)
  start_time = time.time()
  if alg == 'bfs':
    prob = problems.WeightedProblem(initState)
    final_route = breadthFirstSearch(prob)
  elif alg == 'astar':
    prob = problems.AStarProblem(initState)
    final_route = aStarSearch(prob)
  else:
    print 'unknown algorithm'
    return
  end_time = time.time() - start_time
  print "==============================================="
  print final_route
  for busnum, bus in final_route.busses.iteritems():
    graph.set_route(busnum+1, bus.route)
  print 'NODES EXPANDED: %d' % (EXPANDED_NODES)
  print 'TIME: %d' % (end_time)
  graph.draw()
  plt.show()


if __name__ == '__main__':
  alg_name = sys.argv[1]
  main(alg_name)
