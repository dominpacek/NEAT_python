import copy
import random

from neat_genome import Genome, Gene, NeuralNetwork

crossover_rate = 0.8
connection_mutation_rate = 0.3
node_mutation_rate = 0.1
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
    # todo ruletka or something
    fit_sum = 0
    for genome in population:
        fit_sum += genome.fitness
    # for now just choose parents randomly
    while len(new_population) < count:
        if random.random() < crossover_rate:
            parents = random.choices(population, weights=[max(g.fitness, 0.01) for g in population], k=2)
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

    if parents[0].fitness > parents[1].fitness:
        better, worse = parents
    else:
        worse, better = parents

    w_innovations = {}
    for g in worse.genes:
        w_innovations[g.innovation] = g

    child = Genome(better.inputs, better.outputs, better.neuron_count)
    for g in better.genes:
        if g.innovation in w_innovations and random.random() < 0.5:
            child.genes.append(copy.copy(w_innovations[g.innovation]))
        else:
            child.genes.append(copy.copy(g))

    return child


def mutate(genome):
    if random.random() < weight_mutation_rate:
        mutate_weights(genome)

    p = node_mutation_rate
    while p > 0:
        if random.random() < p:
            mutate_node(genome)
        p -= 1

    p = connection_mutation_rate
    while p > 0:
        if random.random() < p:
            mutate_connection(genome)
        p -= 1


def mutate_weights(genome):
    for gene in genome.genes:
        if random.random() < 0.1:
            gene.weight += random.uniform(0.1, 0.1)
            gene.weight = min(1, max(-1, gene.weight))
        else:
            gene.weight = random.uniform(-1, 1)


def mutate_connection(genome):
    in_n = genome.random_neuron(True)
    out_n = genome.random_neuron(False, True)
    # todo make sure recurrent connections are not allowed
    # (or make it a toggle)

    if in_n == out_n:
        # Can't create link to self
        return

    if in_n >= NeuralNetwork.max_neurons:
        # Can't create link from output
        return

    if genome.already_has_gene(in_n, out_n):
        return

    new_link = Gene(in_n, out_n)
    genome.add_gene(new_link)


def mutate_node(genome):
    if len(genome.genes) == 0:
        return

    gene = random.choice(genome.genes)
    gene.enabled = False

    new_node = genome.get_new_neuron_id()
    if new_node == gene.input:
        print("Error: mutate_node INPUT same as new neuron")
    if new_node == gene.output:
        print("Error: mutate_node OUTPUT same as new neuron")
    genome.add_gene(Gene(gene.input, new_node, 1))
    genome.add_gene(Gene(new_node, gene.output, gene.weight))


def next_generation(population):
    new_population = reproduce(population)

    # keep 1 best genome unchanged
    for genome in new_population[1:]:
        mutate(genome)
        genome.generate_nn()

    return new_population
