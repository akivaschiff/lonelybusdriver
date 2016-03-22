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


def test(cityMap, h):
  start_time = time.time()
  problem = problems.BusOperatorVRPProblem(cityMap)
  final_route = aStarSearch(problem, h)
  #import pdb; pdb.set_trace()
  end_time = time.time() - start_time
  #print "==============================================="
  if not final_route:
    #print "NO SOLUTION!"
    return -1
  else:
    #print "SOLUTION:"
    pprint.pprint(final_route)

  #print "==============================================="
  for busnum, bus in enumerate(final_route.busses):
    problem.cityMap.set_route(busnum+1, bus.route)

  #print problem.tmp_storage["cache"]
  #print end_time, final_route.get_state_cost(), problem.expanded
  #assert final_route.get_state_cost() >= max(problem.tmp_storage["cache"])
  return end_time, final_route.get_state_cost(), problem.expanded

def run_simple_test():
  candidates = [total_destination_left_heuristic,
                satisfied_customers,
                onboard_passengers,
                distance_waiting_ratio,
                combined_total_destination_onboard,
                nullHeuristic
                ]


  candidates = [nullHeuristic]
  results = {}
  for h in candidates:
    NUMBER_OF_TESTS = 4
    tmp_result = {}
    for i in range(3, NUMBER_OF_TESTS):
        graph = CityMap.CityMap(r"maps\grid_%d_1" % i)
        #print r"maps\mesh_%d_1" % i
        start_time = time.time()
        end_time = time.time() - start_time
        tmp_result[i] = test(graph, h)
        graph.draw()
        plt.figure(3, figsize=(12,12))
        plt.savefig(r"results\mesh_%d_1_%s.png" % (i, "fw"))
        plt.clf()
        results[h.__name__] = tmp_result
    #print tmp_result
  #print results


def main():
  c = CityMap.CityMap(r'maps\mumford5.map')
  c.draw()
  plt.show()

if __name__ == '__main__':
  main()
