import random

import numpy as np

from simple_alg.genetic_parameters import *


class Genome:
    input_count = -1
    output_count = -1
    _Neuron_innovation = -1

    def __init__(self, input_count, output_count):
        self.input_count = input_count
        self.output_count = output_count

        self.nn = NeuralNetwork(input_count, output_count)

    def mutate(self):
        weights = []
        for matrix in self.nn.weight_matrices:
            weights.append(np.vectorize(mutate_weight)(matrix))
        self.nn.weight_matrices = weights

    def crossover(self, other):
        child = Genome(0, 0)
        for list1, list2 in zip(self.nn.weight_matrices, other.nn.weight_matrices):
            new_list = np.array(
                [np.where(np.random.choice([True, False], size=arr1.shape), arr1, arr2) for arr1, arr2 in
                 zip(list1, list2)])

            child.nn.weight_matrices.append(new_list)
        return child


def mutate_weight(weight):
    if random.random() < mutation_rate:
        if random.random() < weight_perturb_rate:
            weight += random.uniform(-0.1, 0.1)
            return min(1, max(-1, weight))
        else:
            return random.uniform(-1, 1)
    else:
        return weight


class NeuralNetwork:

    # coś nie działa dla innej liczby warstw
    def __init__(self, input_size, output_size, hidden_layers=1, hidden_layer_size=10):

        if input_size == 0 and output_size == 0:
            self.weight_matrices = []
            return

        # weights: input to hidden
        self.weight_matrices = [np.random.rand(input_size, hidden_layer_size) * 2 - 1]

        # weights: hidden to hidden
        self.weight_matrices.extend([np.random.rand(hidden_layer_size, hidden_layer_size) * 2 - 1
                                     for _ in range(hidden_layers - 1)])

        # weights: hidden to output
        self.weight_matrices.append(np.random.rand(hidden_layer_size, output_size) * 2 - 1)

    def evaluate(self, inputs):
        inputs.append(1) # bias
        input_values = (np.array(inputs))

        vector = input_values
        for weights in self.weight_matrices:
            vector = np.dot(vector, weights)
            vector = np.vectorize(steep_sigmoid)(vector)

        return vector


def steep_sigmoid(x):
    weight = 4.9
    s = 1 / (1 + np.exp(-weight * x))

    return s

