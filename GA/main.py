from MapLoader import parse_map
import matplotlib.pyplot as plt
from matplotlib import colors
from evolve import SEAMO2
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        description='Use SEAMO2 to solve the UNRBP\n example:\n\tpython %s --graph Mandl --busses 4 --min 2 --max  10' % __file__)
    parser.add_argument("--graph", help="can be on of the following options: (Mandl, Mumford0)")
    parser.add_argument("--busses", help="number of busses on map", type=int)
    parser.add_argument("--min", help="minimal route length", type=int, default = 2)
    parser.add_argument("--max", help="maximal route length", type = int, default = 10)
    parser.add_argument("--tf", help="transfer penalty time (default to 5 min)", type = int, default = 5)
    parser.add_argument("--initial", help="initial population size", type = int, default = 20)
    parser.add_argument("--generations", help="number of generations to run through", type = int, default = 10)

    problem = parser.parse_args()

    assert problem.min > 1, 'Minimal route must be of length 2'
    assert problem.max > problem.min, 'Maximal route length must be longer than Minimal'
    assert problem.busses > 0, 'You need at least 1 bus :)'
    assert problem.tf >= 0, 'The transfer time between busses must be a non-negative number'
    assert problem.graph in ["Mandl", "Mumford0"], 'Pick an existing map!'

    # define the color list
    cm = plt.get_cmap('gist_rainbow')
    rainbow_colors = [colors.rgb2hex(cm(1.*i/problem.busses)) for i in range(problem.busses)]
    setattr(problem, 'COLORS', rainbow_colors)

    transportNetwork = parse_map(problem.graph)
    print 'Running on map %s with initial population of %s for %s generations' % (problem.graph, problem.initial, problem.generations)
    best = SEAMO2(transportNetwork, problem)
    best.save()
    print best

if __name__ == "__main__":
    main()


sys.exit(0)



'''
Our main algorithm
'''
import cProfile, pstats, StringIO

pr = cProfile.Profile()
pr.enable()
# ... do something ...
transportNetwork = MapLoader.parse_map("Mandl")
best = SEAMO2(transportNetwork, 30, 15)
print best

pr.disable()
#s = StringIO.StringIO()
s = file('GA_stats.txt','w')
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()

sys.exit(0)

'''
The following code demonstrates mutation
'''
transportNetwork = MapLoader.parse_map("Mandl")
population = generate_initial_population(transportNetwork, 1)[0]
population.save()
mutate(population, consts.num_routes, consts.max_route_len, consts.min_route_len)
population.save()
sys.exit(0)

'''
The following code demonstrates a crossover
'''
transportNetwork = MapLoader.parse_map("Mandl")
parent1, parent2 = generate_initial_population(transportNetwork, 2)
offspring = crossover(parent1, parent2, transportNetwork)
offspring.save()
parent1.imagecounter = 101
parent1.save()
parent2.imagecounter = 102
parent2.save()
sys.exit(0)

'''
The following code is for generating images of a solution-generation
'''
transportNetwork = MapLoader.parse_map("Mandl")
population = generate_initial_population(transportNetwork, 1)[0]
rs = Routeset(consts.num_routes, transportNetwork)
for route_num, stop in population.stops_and_route_nums:
    if stop == 'reverse':
        rs.reverse(route_num)
    else:
        rs.add_stop(route_num, stop, True)
rs.show()
sys.exit(0)

# try:
#   child.get_passenger_cost(demand)
# except:
#   print "exception"



