from GenerateRouteset import repair
from GenerateRouteset import generateRouteset
from Generation import crossover, mutate, generate_initial_population
import matplotlib.pyplot as plt
import random
import time
import os
# this line is for ubuntu
if os.path.sep == '/':
    plt.switch_backend('agg')


def SEAMO2(transportNetwork, problem):
    '''
    The main algorithm - detailed description in Paper
    '''
    population_size, generation_count = problem.initial, problem.generations
    population = generate_initial_population(transportNetwork, problem)
    #objectives = ["passengers", "operator"]
    objectives = ["passengers"]
    scores_per_generation = [[] for _ in range(problem.generations)]
    best_objective = min(population, key = lambda x: x.get_scores("passengers"))
    for generation in range(generation_count):
        scores_per_generation[generation] = [p.get_scores("passengers") for p in population]
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
            # if offspring dominates best so far objective
            if offspring.get_scores("passengers") < best_objective.get_scores("passengers"):
                best_objective = offspring
                population[random.choice([parent1_index, parent2_index])] = offspring
            # if offspring dominates either parent
            elif offspring.dominates(parent1):
                #print "offspring dominates parent 1"
                population[parent1_index] = offspring
            elif offspring.dominates(parent2):
                #print "offspring dominates parent 2"
                population[parent2_index] = offspring
            # mutual non domination
            elif not parent1.dominates(offspring) and not parent2.dominates(offspring):
                for ind in range(population_size):
                    if offspring.dominates(population[ind]):
                        population[ind] = offspring
                        break
            # just delete offspring
            else:
                continue

    for gen, scores in enumerate(scores_per_generation):
        plt.plot([gen] * len(scores), scores, 'ro')
    plt.savefig(os.path.join('generating','evolve.png'))
    plt.clf()

    return best_objective
