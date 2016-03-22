import networkx


def total_destination_left_heuristic(state, problem):
  """
  CONSISTENT - admissible

  CONSISTENT if all vertices has same number of passengers

  :param state: the total amount of kilometers left between every passengers and his destination.
  :param problem: VRPProblem.
  :return: returns the sum of all the routes.
  """
  problem.tmp_storage.setdefault("minimal_edge", min([state.graph.get_weight(e) for e in state.graph.g.edges()]))

  total = [problem.tmp_storage["minimal_edge"] for p in state.passengers if not (p.onboard or p.is_arrived())]
  if not total:
    return 0
  return sum(total)


def distance_waiting_ratio(state, problem):
  """
  INCONSISTENT
  :param state:
  :param problem:
  :return: calculate the ratio between total_distance / waiting people
  """
  waiting = len([p for p in state.passengers if not (p.onboard or p.is_arrived())])
  if not waiting or (state.get_state_weight() == 0):
    return 0

  return float(waiting) / state.get_state_weight()

def satisfied_customers(state, problem):
  """
  CONSISTENT
  :param state:
  :param problem:
  :return: TOTAL_PASSENGERS - NUMBER_OF_SATISFIED_PASSENGERS
  """
  return len(problem.cityMap.passengers) - [p.is_arrived() for p in state.passengers].count(True)


def onboard_passengers(state, problem):
  """
  CONSISTENT
  :param state:
  :param problem:
  :return: TOTAL_PASSENGERS_UNSATISFIED - NUMBER_OF_ONBOARD_PASSENGERS
  """
  unsat = [p.is_arrived() for p in state.passengers].count(False)
  sat = len(state.passengers) - unsat
  onboard = [p for p in state.passengers if p.onboard]
  return unsat - (len(onboard) + sat)


def combined_total_destination_onboard(state, problem):
  """
  NOT CONSISTENT...
  :param state:
  :param problem:
  :return:
  """
  return onboard_passengers(state, problem) + total_destination_left_heuristic(state, problem)