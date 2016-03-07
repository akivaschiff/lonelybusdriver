import itertools

class Problem:
  def __init__(self, initialState):
    self.initialState = initialState

  def getStartState(self):
    return self.initialState

  def isGoalState(self, state):
    #return len(state.covered) == len(state.graph)
    return all([p.is_arrived() for p in state.passengers])

  def getSuccessors(self, state):
    raise NotImplemented()

class WeightedProblem(Problem):

  def __init__(self, initialState):
    Problem.__init__(self, initialState)

  def getSuccessors(self, state):
    if self.isGoalState(state):
      return []

    successorStates = []
    allNewStops = {}
    # find the bus with the minimal destination..
    shortest_bus = state.getShortestBus()
    # get the last bus stop
    recent_stop = shortest_bus.route[-1]
    for new_stop in state.graph.get_neighbors(recent_stop):
      weight_to_stop = state.graph.get_weight((recent_stop, new_stop))
      newState = state.getCopy()
      newState.addStop(shortest_bus, new_stop, weight_to_stop)
      #successorStates.append((newState, new_stop))
      successorStates.append(newState)

    return successorStates