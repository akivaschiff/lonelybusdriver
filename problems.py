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

class PolyweightProblem(Problem):
  def getSuccessors(self, state):
    successorStates = []
    allNewStops = {}
    for busIndex, busRoute in state.busses.iteritems():
      newStops = state.graph.get_neighbors(busRoute[-1])
      #if len(busRoute) > 1:
      #  newStops.remove(busRoute[-2])
      allNewStops[busIndex] = newStops

    for newStopPerBus in itertools.product(*allNewStops.values()):
      newState = state.getCopy(newStopPerBus)
      successorStates.append((newState, newStopPerBus))
    #print successorStates
    #raw_input()
    return successorStates

class UniweightProblem(Problem):
  def getSuccessors(self, state):
    successorStates = []
    allNewStops = {}
    for busIndex, busRoute in state.busses.iteritems():
      newStops = state.graph.get_neighbors(busRoute[-1])
      #if len(busRoute) > 1:
      #  newStops.remove(busRoute[-2])
      allNewStops[busIndex] = newStops

    for newStopPerBus in itertools.product(*allNewStops.values()):
      newState = state.copyAdvanceAllBusses(newStopPerBus)
      successorStates.append((newState, newStopPerBus))
    #print successorStates
    #raw_input()
    return successorStates
