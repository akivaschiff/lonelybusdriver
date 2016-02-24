import copy
import util
import pprint
import itertools
import problems
import CityMap

class RoutesState:
  def __init__(self, graph, numBusses, finalStop):
    self.graph = graph
    self.busses = {}
    self.finalStop = finalStop
    self.covered = set()
    self.covered.add(finalStop)
    for i in range(numBusses):
      self.busses[i] = (finalStop,)
  def copyAdvanceAllBusses(self, newStops):
    newState = RoutesState(self.graph, len(self.busses), self.finalStop)
    newState.covered = set(self.covered)
    for i, stop in enumerate(newStops):
        if not stop:
          continue
        newState.busses[i] = self.busses[i] + (stop,)
        newState.covered.add(stop)
    return newState
  def copyAdvanceOneBus(self, index, newStop):
    newState = RoutesState(self.graph, len(self.busses), self.finalStop)
    newState.covered = set(self.covered)
    newState.busses = copy.deepcopy(self.busses)
    newState.busses[index] = newState.busses[index] + (newStop,)
    newState.covered.add(stop)
    return newState
  def __hash__(self):
    return hash(tuple(self.busses.values()))
  def __repr__(self):
    return str(self.busses) + " " + str(self.covered)


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  nodes = util.Queue()
  directions = util.Queue()
  nodes.push(problem.getStartState())
  directions.push([])
  seen = []

  while not nodes.isEmpty():
    current_node = nodes.pop()
    path = directions.pop()
    # if we've already reached this point in the graph before - move on
    if current_node in seen:
        continue
    seen.append(current_node)
    if problem.isGoalState(current_node):
        # we found the goal!
        return path
    new_states = problem.getSuccessors(current_node)
    new_states = [s for s in new_states if s[0] not in seen]
    for state in new_states:
        nodes.push(state[0])
        directions.push(path+[state[1]])


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
  nodes = util.PriorityQueue()
  directions = util.PriorityQueue()
  nodes.push((problem.getStartState(),[],0),0)
  seen = []
  import pprint
  while not nodes.isEmpty():
    current_node, path, current_cost = nodes.pop()
    #print('>>> current: %s, cost: %s, path: %s' % (str(current_node),current_cost,path))
    # if we've already reached this point in the graph before - move on
    if current_node in seen:
        continue
    seen.append(current_node)
    if problem.isGoalState(current_node):
        # we found the goal!
        return path
    new_states = problem.getSuccessors(current_node)
    new_states = [s for s in new_states if s[0] not in seen][::-1]
    for state, direction, cost in new_states:
        new_cost = current_cost + cost + heuristic(state, problem)
        nodes.push((state,path+[direction],current_cost+cost),new_cost)

  return []

def cornersHeuristic(state, problem):
  pass


def main():
  graph = CityMap.CityMap("map1.txt")
  initState = RoutesState(graph, 1, graph.final_station)
  prob = problems.UniweightProblem(initState)
  path = breadthFirstSearch(prob)
  pprint.pprint([(graph.final_station,)] + path)


if __name__ == '__main__':
  main()
