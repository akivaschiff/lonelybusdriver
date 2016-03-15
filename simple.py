import sys
import time
import util
import pprint
import problems
import CityMap
import matplotlib.pyplot as plt

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
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

    #print current_state, current_state.get_state_weight()
    if problem.isGoalState(current_state):
        print current_state.get_state_weight()
        return current_state

    for state in (s for s in problem.getSuccessors(current_state) if s not in seen):
      state_cost = state.get_state_weight() + heuristic(state, problem)
      nodes.push(state, state_cost)

    seen.add(current_state)

  return []


def test(alg, cityMap):
  start_time = time.time()
  problem = problems.VRPProblem(cityMap)
  if alg == 'astar':
    final_route = aStarSearch(problem)
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

  print 'NODES EXPANDED: %d' % (problem.expanded)
  print 'TIME: %d' % (end_time)
  print "==============================================="
  for busnum, bus in enumerate(final_route.busses):
    problem.cityMap.set_route(busnum+1, bus.route)
  return (end_time, final_route.get_state_weight(), problem.expanded)

def run_simple_test(alg):
  NUMBER_OF_TESTS = 10
  result = {}
  for i in range(1, 2):
    graph = CityMap.CityMap(r"maps\random_9_1")
    print r"maps\mesh_%d_1" % i
    result[i] = test(alg, graph)
    graph.draw()
    plt.show()
  return result


def main(alg = 'bfs'):
  #graph = CityMap.CityMap("maps\\5ring3bus.txt")
  print run_simple_test(alg)


if __name__ == '__main__':
  alg_name = sys.argv[1]
  main(alg_name)
