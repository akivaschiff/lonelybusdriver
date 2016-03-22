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

class GenStat:
    def __init__(self, gen_num, gen_size):
        self.generation_size = gen_size
        self.generation_number = gen_num
        self.all_scores = []
        self.best_score = float('inf')
        self.average_score = 0
        self.offs_bad = 0
        self.offs_dominates_parent = 0
        self.offs_best_news = 0
        self.offs_replace_other = 0
        self.offs_thrown_away = 0
    def get_params(self):
        self.property_names = ['best_score','average_score'] + [fn for fn in dir(self) if fn.startswith('offs')]
        return [getattr(self, fn) for fn in self.property_names]
    def finalize(self):
        self.best_score = min(self.all_scores)
        self.average_score = sum(self.all_scores) / len(self.all_scores)
        for param in dir(self):
            if param.startswith('offs'):
                setattr(self, param, getattr(self, param) / float(self.generation_size))

def SEAMO2(transportNetwork, problem):
    '''
    The main algorithm - detailed description in Paper
    '''
    population_size, generation_count = problem.initial, problem.generations
    population = generate_initial_population(transportNetwork, problem)
    #objectives = ["passengers", "operator"]
    objectives = ["passengers"]

    scores_per_generation = [[] for _ in range(problem.generations)]
    gen_stats = []

    best_objective = min(population, key = lambda x: x.get_scores("passengers"))
    for generation in range(generation_count):
        gen_stats.append(GenStat(generation, population_size))
        print "new generation", generation
        for parent1_index in range(population_size):
            # select parent 1
            parent1 = population[parent1_index]
            gen_stats[-1].all_scores.append(parent1.get_scores("passengers"))
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
                gen_stats[-1].offs_bad += 1
                continue
            # this is a heavy function
            offspring.calc_scores()

            # insert offspring into population
            if offspring in population:
                continue
            # if offspring dominates best so far objective
            if offspring.get_scores("passengers") < best_objective.get_scores("passengers"):
                gen_stats[-1].offs_best_news += 1
                best_objective = offspring
                population[random.choice([parent1_index, parent2_index])] = offspring
            # if offspring dominates either parent
            elif offspring.dominates(parent1):
                #print "offspring dominates parent 1"
                gen_stats[-1].offs_dominates_parent += 1
                population[parent1_index] = offspring
            elif offspring.dominates(parent2):
                #print "offspring dominates parent 2"
                gen_stats[-1].offs_dominates_parent += 1
                population[parent2_index] = offspring
            # mutual non domination
            elif not parent1.dominates(offspring) and not parent2.dominates(offspring):
                for ind in range(population_size):
                    if offspring.dominates(population[ind]):
                        gen_stats[-1].offs_replace_other += 1
                        population[ind] = offspring
                        break
            # just delete offspring
            else:
                gen_stats[-1].offs_thrown_away += 1
                continue
        gen_stats[-1].finalize()

    datas = zip(*[stat.get_params() for stat in gen_stats])
    labels = gen_stats[0].property_names
    for i, data in enumerate(datas):
        plt.plot(range(len(data)), data, label = labels[i], marker = 'o', linestyle = 'o')
    plt.legend()
    plt.savefig(os.path.join('generating','stats.png'))
    plt.clf()

    for gen, scores in enumerate(scores_per_generation):
        plt.plot([gen] * len(scores), scores, 'ro')
    plt.savefig(os.path.join('generating','evolve.png'))
    plt.clf()

    return best_objective, gen_stats
