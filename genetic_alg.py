import random

from genome import Genome, Gene

crossover_rate = 0.8
connection_mutation_rate = 0.05
node_mutation_rate = 0.03
weight_mutation_rate = 0.8


def generate_new_population(count, inputs, outputs):
    population = []

    for i in range(count):
        g = Genome(inputs, outputs)
        mutate(g)
        population.append(g)
    for genome in population:
        genome.generate_nn()
    return population


def reproduce(population):
    count = len(population)
    population = sorted(population, key=lambda g: g.fitness, reverse=True)
    population = population[:(count // 2)]

    new_population = [population[0], population[1]]
    #todo ruletka or something
    fit_sum = 0
    for genome in population:
        fit_sum += genome.fitness
    # for now just choose parents randomly
    while len(new_population) < count:
        if random.random() < crossover_rate:
            parents = random.choices(population, weights=[g.fitness + 0.01 for g in population], k=2)
            new_population.append(crossover(parents))
        else:
            new_population.append(random.choice(population))

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

    if parents[0].fitness > parents[1].fitness:
        better, worse = parents
    else:
        worse, better = parents

    w_innovations = {}
    for g in worse.genes:
        w_innovations[g.innovation] = g

    child = Genome(better.inputs, better.outputs)
    for g in better.genes:
        if g.innovation in w_innovations and random.random() < 0.5:
            child.genes.append(w_innovations[g.innovation])
        else:
           child.genes.append(g)

    return child


def mutate(genome):
    if random.random() < weight_mutation_rate:
        mutate_weights(genome)

    if random.random() < node_mutation_rate:
        mutate_node(genome)

    if random.random() < connection_mutation_rate:
        mutate_connection(genome)


def mutate_weights(genome):
    for gene in genome.genes:
        if random.random() < 0.1:
            gene.weight += random.uniform(0.1, 0.1)
            gene.weight = min(1, max(-1, gene.weight))
        else:
            gene.weight = random.uniform(-1, 1)


def mutate_connection(genome):
    n1 = genome.random_neuron(True)
    n2 = genome.random_neuron()

    if n1 == n2:
        # Can't create link to self
        return

    if genome.already_has_gene(n1, n2):
        return

    new_link = Gene(n1, n2)
    genome.add_gene(new_link)


def mutate_node(genome):
    if len(genome.genes) == 0:
        return

    gene = random.choice(genome.genes)
    gene.enabled = False

    new_neuron = genome.add_neuron()
    genome.add_gene(Gene(gene.input, new_neuron))
    genome.add_gene(Gene(new_neuron, gene.output, gene.weight))

def next_generation(population):
    new_population = reproduce(population)

    for genome in new_population:
        mutate(genome)
        genome.generate_nn()

    return new_population
