import itertools

class Problem:
  def __init__(self, initialState):
    self.initialState = initialState
  def getStartState(self):
    return self.initialState
  def isGoalState(self, state):
    return len(state.covered) == len(state.graph)
  def getSuccessors(self, state):
    raise Exception

class WeightedProblem(Problem):
  def getSuccessors(self, state):
    successorStates = []
    allNewStops = {}
    shortest_bus = state.getShortestBus()
    recent_stop = shortest_bus.route[-1]
    for new_stop in state.graph.get_neighbors(recent_stop):
      weight_to_stop = state.graph.get_weight((recent_stop, new_stop))
      newState = state.getCopy()
      newState.addStop(shortest_bus, new_stop, weight_to_stop)
      successorStates.append((newState, new_stop))
    return successorStates