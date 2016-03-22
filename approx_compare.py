import clustering_cool_solution
import CityMap
import glob
import time

def runTest(algo, n):
  res = {}
  maps = glob.glob(r"maps\many\*")
  for i, m in enumerate(maps):
    if i == n-1:
      break
    print m
    city = CityMap.CityMap(m)
    strat = time.time()
    r = algo(city)
    end = time.time() - strat
    res[i] = (end, city.get_total_cost())
    print res
  return res


def main():
  algo = [
    clustering_cool_solution.floyd_warshall_solution_remove_stations,
    clustering_cool_solution.hub_algo
  ]
  res = {}
  number_of_tests = 20
  for alg in algo:
    res[alg.__name__] = runTest(alg, number_of_tests)
  print res

if __name__ == "__main__":
  main()