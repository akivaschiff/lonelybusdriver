import problems
import CityMap
import util
import time
import matplotlib.pyplot as plt

def null(state, problem):
  """
  CONSISTENT

  :param state: the total amount of kilometers left between every passengers and his destination.
  :param problem: VRPProblem.
  :return: returns the sum of all the routes.
  """
  return 0


def satisfied_heuristic(state, problem):
  """
  very bad...
  :param state:
  :param problem:
  :return:
  """
  return len(state.passengers) - len([p for p in state.passengers if p.is_arrived()])


def onboard_heuristic(state, problem):
  """
  probably admissable
  :param state:
  :param problem:
  :return:
  """
  if problem.isGoalState(state):
    return 0
  l = len([p for p in state.passengers if p.onboard])
  if not l:
    return 1
  return 1.0 / l


def maximal_destination_for_passenger(state, problem):
  """
  probably inadmissible - also bad...
  :param state:
  :param problem:
  :return:
  """
  unsatisfied = [p for p in state.passengers if not (p.is_arrived() or p.onboard)]
  if unsatisfied:
     max_dist = max([p.opt for p in unsatisfied])
     return max_dist
  return 0


def euclid_destination_for_passenger(state, problem):
  """
  probably inadmissible - also bad...
  :param state:
  :param problem:
  :return:
  """
  unsatisfied = [p for p in state.passengers if not (p.is_arrived() or p.onboard)]
  if unsatisfied:
     max_dist = sum([p.opt for p in unsatisfied])
     return max_dist
  return 0


def aStarSearch(problem, heuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  nodes = util.PriorityQueue()
  nodes.push(problem.getStartState(), 0)

  seen = set()
  while not nodes.isEmpty():
    current_state = nodes.pop()
    #print current_state
    if current_state in seen:
      continue

    if problem.isGoalState(current_state):
        return current_state

    for state in (s for s in problem.getSuccessors(current_state) if s not in seen):
      state_cost = problem.getStateCost(state) + heuristic(state, problem)
      nodes.push(state, state_cost)
    seen.add(current_state)

  return []


def test_heuristics():
  heu = [
    euclid_destination_for_passenger,
  ]
  results = {}
  for h in heu:
    tmp = {}
    for i in range(1, 5):
      tmp[i] = run_test(i, h)
    results[h.__name__] = tmp

  print results

def run_test(i, h):
  print r'maps\grid_10_1_pss_%d' % i
  city = CityMap.CityMap(r'maps\grid_10_1_pss_%d' % i)
  start = time.time()
  problem = problems.PassengersMinimalTravelVRPProblem(city)
  r = aStarSearch(problem, onboard_heuristic)
  end = time.time() - start
  # print r, r.get_state_cost()
  # city.set_route(1, r.busses[0].route)
  # city.draw()
  # plt.figure(3, figsize=(12,12))
  # plt.show()
  return end, problem.expanded

def all_solutions():
  city = CityMap.CityMap(r'maps\grid_4_1')
  problem = problems.PassengersMinimalTravelVRPProblem(city)
  r = aStarSearch(problem, onboard_heuristic)
  for i, s in enumerate(sol):
    city.set_route(1, s.busses[0].route)
    city.draw()
    plt.figure(3, figsize=(12,12))
    plt.savefig(r"results\pass\grid_4_solution_%d.png" % i)
    plt.clf()

def main():
  test_heuristics()
  exit()
  city = CityMap.CityMap(r'maps\grid_4_1')
  city.set_route(1, [])
  city.draw()
  plt.figure(3, figsize=(12,12))
  plt.savefig(r"results\pass\grid_4_start.png")
  plt.clf()
  problem = problems.PassengersMinimalTravelVRPProblem(city)
  s = problem.getStartState()
  for ss in problem.getSuccessors(s):
    for i, sss in enumerate(problem.getSuccessors(ss)):
      city.set_route(1, sss.busses[0].route)
      city.draw()
      plt.figure(3, figsize=(12,12))
      plt.savefig(r"results\pass\grid_4_start_%d.png" % i)
      plt.clf()

if __name__ == "__main__":
  main()