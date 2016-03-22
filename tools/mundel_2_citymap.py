import json
import sys

def parse_coordinates(coordinates_fd):
  res = []
  for i, line in enumerate(coordinates_fd):
    if i:
      x, y = line.strip().split(" ")
      res.append([str(i-1), float(x), float(y)])
  return res


def parse_demand(demand_fd):
  psngrs = []
  i=0
  for line in demand_fd:
    if line.strip():
      j = 0
      for d in line.strip().split(" "):
        if not d:
          continue
        if d != "0":
          psngrs.append([str(i), str(j)])
        j += 1
      i += 1
  return psngrs


def parse_TravelTimes(tt_fd):
  roads = []
  i=0
  for line in tt_fd:
    if line.strip():
      j = 0
      for distance in line.strip().split(" "):
        if not distance:
          continue
        if (distance != "0") and (distance != "Inf"):
          roads.append([str(i), str(j)])
        j += 1
      i += 1
  return roads


def main():
  with open(sys.argv[2], "r") as tt:
    roads = parse_TravelTimes(tt)

  with open(sys.argv[1], "r") as coordinate:
    nodes = parse_coordinates(coordinate)

  with open(sys.argv[3], "r") as demand:
    passn = parse_demand(demand)

  with open(sys.argv[5], "w") as out:
    json.dump({
      "stations" : nodes,
      "roads" : roads,
      "passengers" : passn,
      "lines" : int(sys.argv[4])
    }, out)

if __name__ == "__main__":
  main()