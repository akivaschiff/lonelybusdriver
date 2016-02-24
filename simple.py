import copy
import utils
import pprint
import itertools

class RoutesState:
  def __init__(self, graph, numBusses, finalStop):
    self.graph = graph
    self.busses = {}
    self.finalStop = finalStop
    self.covered = set()
    self.covered.add(finalStop)
    for i in range(numBusses):
      self.busses[i] = (finalStop,)
  def getCopy(self, newStops):
    newState = RoutesState(self.graph, len(self.busses), self.finalStop)
    newState.covered = set(self.covered)
    for i, stop in enumerate(newStopPerBus):
        newState.busses[i] = self.busses[i] + (stop,)
        newState.covered.add(stop)
  def __hash__(self):
    return hash(tuple(self.busses.values()))

class UniweightProblem:
  def __init__(self, initialState):
    self.initialState = initialState
  def getStartState(self):
    return self.initialState.finalStop
  def isGoalState(self, state):
    return len(state.covered) == len(state.graph)
  def getSuccessors(self, state):
    successorStates = []
    allNewStops = {}
    for busIndex, busRoute in state.busses.iteritems():
      if len(busRoute) > 1:
        newStops = state.graph.getChildren(busRoute[-1], busRoute[-2])
      else:
        newStops = state.graph.getChildren(busRoute[-1])
      allNewStops[busIndex] = newStops

    for newStopPerBus in itertools.product(newStops.values())
      newState = state.getCopy(newStopPerBus)
      successorStates.append((newState, newStopPerBus))

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

def main():
  graph = pass
  goal = pass
  initState = RoutesState(graph, 1, goal)
  problem = UniweightProblem(initState)
  path = breadthFirstSearch(problem)
  pprint.pprint(path)


if __name__ == '__main__':
  main()