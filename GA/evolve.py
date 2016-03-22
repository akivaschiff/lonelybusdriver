from GenerateRouteset import repair
from GenerateRouteset import generateRouteset
from Generation import crossover, mutate, generate_initial_population
import random
import time


def SEAMO2(transportNetwork, problem):
    '''
    The main algorithm - detailed description in Paper
    '''
    population_size, generation_count = problem.initial, problem.generations
    population = generate_initial_population(transportNetwork, problem)
    objectives = ["passengers", "operator"]
    best_objective = {obj_name: min(population, key = lambda x: x.scores[obj_name]) for obj_name in objectives}
    #print [best_objective[key].get_scores() for key in objectives]
    for generation in range(generation_count):
        print "new generation", generation
        for parent1_index in range(population_size):
            # select parent 1
            parent1 = population[parent1_index]
            # select parent 2
            parent2_index = random.randint(0, population_size - 1)
            parent2 = population[parent2_index]
            # generate an offspring
            offspring = crossover(parent1, parent2, transportNetwork, problem)

            # repair the offspring - this shouldn't be necessary
            repair(offspring, transportNetwork, problem.max, problem.min)

            # apply mutation - gamma ray radiation
            mutate(offspring, problem.busses, problem.max, problem.min)
            if len(offspring.covered) < len(offspring.transportNetwork.nodes()):
                continue
            # this is a heavy function
            offspring.calc_scores()

            # insert offspring into population
            if offspring in population:
                continue
            # if offspring dominates either parent
            elif offspring.dominates(parent1):
                #print "offspring dominates parent 1"
                population[parent1_index] = offspring
            elif offspring.dominates(parent2):
                #print "offspring dominates parent 2"
                population[parent2_index] = offspring
            # if offspring dominates best so far objective
            elif offspring.get_scores()["passengers"] < best_objective["passengers"].get_scores()["passengers"]:
                best_objective["passengers"] = offspring
                if not parent1 == best_objective["operator"]:
                    population[parent1_index] = offspring
                elif not parent2 == best_objective["operator"]:
                    population[parent2_index] = offspring
            elif offspring.get_scores()["operator"] < best_objective["operator"].get_scores()["operator"]:
                best_objective["operator"] = offspring
                if not parent1 == best_objective["passengers"]:
                    population[parent1_index] = offspring
                elif not parent2 == best_objective["passengers"]:
                    population[parent2_index] = offspring
            # mutual non dominatoion
            elif not parent1.dominates(offspring) and not parent2.dominates(offspring):
                for ind in range(population_size):
                    if offspring.dominates(population[ind]):
                        population[ind] = offspring
                        break
            # just delete offspring
            else:
                continue
    return best_objective
