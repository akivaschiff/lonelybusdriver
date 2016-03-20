import networkx


class Passenger:
  """
  represent a passenger in our world. has source station, destination
  and boolean value - is arrived?
  """
  def __init__(self, source, dest, graph, onboard=False, arrived=False, distance=0):
    self.src = source
    self.dst = dest
    self.distance = distance
    self.arrived = arrived or (source == dest)
    self.opt = graph.euclid_distance_by_name(source, dest)
    self.onboard = onboard

  def get_travel(self):
    return self.distance

  def get_optimal_distance(self):
    return self.opt

  def is_arrived(self):
    return self.arrived

  def __hash__(self):
    return hash((self.src, self.dst, self.arrived, self.onboard, self.distance))


class Bus:
  def __init__(self, route=None, weight=0):
    self.route = route if route else ()
    # this data structure is for quickly checking if an edge is in our route
    self.edges = frozenset([(self.route[i], self.route[i+1]) for i in range(len(self.route)-1)])
    self.weight = weight

  def build_edge_list(self):
    return [(self.route[i], self.route[i+1]) for i in range(len(self.route)-1)]

  def __hash__(self):
    return hash(self.edges)


class RoutesState:
  """
  RouteState = represent a state in the search, (it's an immutable object).
  """
  def __init__(self, graph, passengers=None, busses=None, routes=None):
    self.graph = graph
    self.passengers = tuple(Passenger(s, d, graph) for s, d in graph.passengers) if (not passengers) else passengers
    self.busses = tuple(Bus() for i in range(self.graph.number_of_busses)) if (not busses) else busses
    self.routes = routes if routes else frozenset()

  def getShortestBus(self):
    return min(self.busses, key=lambda x: x.weight)

  def _create_new_route(self, bus, stop, weight):
    new_busses = []
    for b in self.busses:
      if b == bus:
        if b.route and (b.route[-1], stop) in bus.edges:
          return None
        else:
          new_busses.append(Bus(b.route + tuple(stop), b.weight + weight))
      else:
        new_busses.append(Bus(b.route, b.weight))
    return new_busses

  def _create_new_passengers(self, bus, stop, weight):
    new_passengers = []
    for p in self.passengers:
      if (stop == p.dst) and (p.src in bus.route):
        # final stop for passenger
        new_passengers.append(Passenger(p.src, p.dst, self.graph,
                                        onboard=False, arrived=True, distance=p.distance + weight))
      elif (stop == p.src) and (not p.onboard):
        # first stop for the passenger
        new_passengers.append(Passenger(p.src, p.dst, self.graph, onboard=bus, arrived=(stop == p.dst), distance=0))
      elif p.onboard == bus:
        new_passengers.append(Passenger(p.src, p.dst, self.graph,
                                        onboard=bus, arrived=False, distance=p.distance + weight))
      else:
        new_passengers.append(Passenger(p.src, p.dst, self.graph, p.onboard, p.arrived, p.distance))
    return new_passengers

  def create_new_route_state(self, bus, stop, weight):
    new_busses = self._create_new_route(bus, stop, weight)
    if not new_busses:
      return None
    new_passengers = self._create_new_passengers(bus, stop, weight)
    return RoutesState(self.graph, tuple(new_passengers), tuple(new_busses), frozenset(stop))

  def create_new_route_state_from_route(self, bus, route, weight):
    stop = route[-1]
    if (bus.route[-1], stop) in self.routes:
      return None
    new_busses = []
    for b in self.busses:
      if b == bus:
        new_busses.append(Bus(b.route + tuple(route), b.weight + weight))
      else:
        new_busses.append(Bus(b.route, b.weight))

    new_passengers = self._create_new_passengers(bus, stop, weight)
    return RoutesState(self.graph, tuple(new_passengers), tuple(new_busses),
                       frozenset(set(self.routes) |  {((bus.route[-1], stop))}))

  def get_route_weight(self, line_number):
    return sum([self.graph.get_weight(edge) for edge in line_number.build_edge_list()])

  def get_state_cost(self):
    return self.get_state_weight()

  def get_state_weight(self):
    """
    calculate the entire state.
    """
    return sum([self.get_route_weight(line) for line in self.busses])

  def __hash__(self):
    if self.routes:
      return hash(self.routes)
    return hash((hash(self.busses), hash(self.passengers)))

  def __eq__(self, other):
    return hash(self) == hash(other)

  def __repr__(self):
    return ", ".join([str(b) + ': ' + str(self.busses[b].route) for b in range(len(self.busses))])


class Problem:
  def __init__(self):
    self.expanded = 0
    self.tmp_storage = {}

  def getStartState(self):
    raise NotImplemented()

  def isGoalState(self, state):
    raise NotImplemented()

  def getSuccessors(self, state):
    raise NotImplemented()

  def getStateCost(self, state):
    raise NotImplemented()


class VRPProblem(Problem):
  """
  Implementation of the VRP problem
  """
  def __init__(self, cityMap):
    Problem.__init__(self)
    self.cityMap = cityMap

  def isGoalState(self, state):
    return all([p.is_arrived() for p in state.passengers])

  def getStartState(self):
    return RoutesState(self.cityMap)

  def getSuccessors(self, state):
    self.expanded += 1
    successorStates = []
    # find the bus with the minimal destination..
    shortest_bus = state.getShortestBus()
    if not shortest_bus.route:
      return [state.create_new_route_state(shortest_bus, [node], 0) for node in self.cityMap.g.nodes()]

    # get the last bus stop
    recent_stop = shortest_bus.route[-1]
    for new_stop in state.graph.get_neighbors(recent_stop):
      weight_to_stop = state.graph.get_weight((recent_stop, new_stop))
      n = state.create_new_route_state(shortest_bus, new_stop, weight_to_stop)
      if n:
        successorStates.append(n)

    return successorStates


class BusOperatorVRPProblem(VRPProblem):
  """
  Represent a Bus Operator problem. where the destination for each bus matters!
  """
  def __init__(self, cityMap):
    VRPProblem.__init__(self, cityMap)

  def getStateCost(self, state):
    return state.get_state_cost()


class PassengersMinimalTravelVRPProblem(VRPProblem):
  def __init__(self, cityMap):
    VRPProblem.__init__(self, cityMap)
    self.src_nodes = {s for s, d in cityMap.passengers}
    print self.src_nodes
    self.relevant_nodes = {d for s, d in cityMap.passengers} | self.src_nodes
    print self.relevant_nodes - self.src_nodes
    self.short_path = networkx.all_pairs_dijkstra_path(cityMap.g)

  def isGoalState(self, state):
    if self.expanded > 30000:
      return True
    return all([p.is_arrived() for p in state.passengers])

  def getStateCost(self, state):
    return sum([p.distance for p in state.passengers]) + state.get_state_cost()

  def getSuccessors(self, state):
    self.expanded += 1
    successorStates = []
    # find the bus with the minimal destination..
    shortest_bus = state.getShortestBus()
    if not shortest_bus.route:
      return [state.create_new_route_state(shortest_bus, [node], 0) for node in self.src_nodes]

    # get the last bus stop
    recent_stop = shortest_bus.route[-1]
    for node in self.relevant_nodes:
      if node == recent_stop:
        continue
      p = self.short_path[recent_stop][node][1:]
      w = state.graph.get_route_weight_from_route(p)
      n = state.create_new_route_state_from_route(shortest_bus, p, w)
      if n:
        successorStates.append(n)

    return successorStates