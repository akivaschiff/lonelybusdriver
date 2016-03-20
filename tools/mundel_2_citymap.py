import json
import sys

def parse_coordinates(coordinates_fd):
  res = []
  for i, line in enumerate(coordinates_fd):
    if i:
      x, y = line.strip().split(" ")
      res.append([str(i), float(x), float(y)])
  return res


def parse_demand(demand_fd):
  pass

def parse_TravelTimes(tt_fd):
  roads = []
  for i, line in enumerate(tt_fd):
    for j, distance in enumerate(line.strip().split("    ")):
      if (distance != "0") and (distance != "inf"):
        roads.append([str(i), str(j)])
  return roads


def main():
  with open(sys.argv[2], "r") as tt:
    roads = parse_TravelTimes(tt)

  with open(sys.argv[1], "r") as coordinate:
    nodes = parse_coordinates(coordinate)

  with open(sys.argv[3], "w") as out:
    json.dump({}, out)

if __name__ == "__main__":
  main()