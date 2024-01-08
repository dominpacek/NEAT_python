import copy

from standard_genetic.genome import *

# Used to assign the same innovation number to reoccurring mutations
# keys are tuples (in_node, out_node), values are innovation numbers
# e.g. {(1, 2): 1, (2, 3): 2}
new_connections_this_generation = {}
new_nodes_this_generation = {}


def generate_new_population(count, inputs, outputs, connected=False):
    population = []

    for i in range(count):
        g = Genome(inputs, outputs)
        population.append(g)
    return population


def reproduce(population):
    count = len(population)
    population = sorted(population, key=lambda g: g.fitness, reverse=True)
    population = population[:(count // 2)]

    # Keep 2 best genomes
    new_population = [population[0], population[1]]
    fit_sum = 0
    for i in range(count//10):
        new_population.append(Genome(population[0].input_count, population[0].output_count))
    for genome in population:
        fit_sum += genome.fitness
    while len(new_population) < count:
        if random.random() < crossover_rate:
            parents = random.choices(population, weights=[max(g.fitness, 0.001) for g in population], k=2)
            new_population.append(crossover(parents))
        else:
            new_population.append(copy.deepcopy(random.choice(population)))

    types = {}
    for g in new_population:
        t = type(g)
        if t not in types:
            types[t] = 1
        else:
            types[t] += 1

    return new_population


def crossover(parents):
    if len(parents) != 2:
        raise Exception('Crossover needs exactly two parents')

    child = parents[0].crossover(parents[1])
    return child


def next_generation(population):
    new_population = reproduce(population)

    # Keep the best genome not mutated
    for genome in new_population[1:]:
        genome.mutate()

    return new_population
