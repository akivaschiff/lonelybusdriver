import time
import util
import pprint
import problems
import CityMap
import matplotlib.pyplot as plt
from mesh_heuristics import *


def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  CONSISTENT
  """
  return 0



def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  nodes = util.PriorityQueue()
  nodes.push(problem.getStartState(), 0)

  seen = set()
  while not nodes.isEmpty():
    current_state = nodes.pop()
    if current_state in seen:
      continue

    if problem.isGoalState(current_state):
        return current_state

    for state in (s for s in problem.getSuccessors(current_state) if s not in seen):
      state_cost = problem.getStateCost(state) + heuristic(state, problem)
      nodes.push(state, state_cost)

    seen.add(current_state)

  return []

