import random

import numpy as np


class Genome:
    inputs = -1
    outputs = -1

    def __init__(self, inputs, outputs):
        # inputs and outputs are ints
        self.inputs = inputs
        self.outputs = outputs
        self.neurons = inputs
        self.genes = []
        self.nn = None
        if Genome.inputs == -1:
            Genome.inputs = inputs
        if Genome.outputs == -1:
            Genome.outputs = outputs

    def add_gene(self, gene):
        self.genes.append(gene)

    def add_neuron(self):
        self.neurons += 1
        return self.neurons - 1

    def random_neuron(self, inputs_allowed=False):
        neurons = {}
        if inputs_allowed:
            for i in range(self.inputs):
                neurons[i] = True
        for o in range(self.outputs):
            neurons[NeuralNetwork.max_neurons + o] = True
        for gene in self.genes:
            if inputs_allowed or gene.input > self.inputs:
                neurons[gene.input] = True
            neurons[gene.output] = True

        neuron = np.random.choice(list(neurons.keys()))
        return neuron

    def generate_nn(self):
        self.nn = NeuralNetwork(self)

    def already_has_gene(self, input, output):
        for gene in self.genes:
            if gene.input == input and gene.output == output:
                return True
        return False


class Neuron:
    def __init__(self, id):
        self.value = 0
        self.id = id
        self.incoming = []


class Gene:
    _Innovation = 0

    def __init__(self, input, output, weight=random.random(), increase_innovation=True, enabled=True):
        self.input = input
        self.output = output
        self.weight = weight
        self.enabled = enabled
        if increase_innovation:
            Gene._Innovation += 1
            # ? not sure about this if statement
        self.innovation = Gene._Innovation


class NeuralNetwork:
    max_neurons = 1000000

    def __init__(self, genome):
        self.neurons = {}
        self.inputs = genome.inputs
        self.outputs = genome.outputs

        for i in range(genome.inputs):
            self.neurons[i] = Neuron(i)
        for o in range(genome.outputs):
            self.neurons[NeuralNetwork.max_neurons + o] = Neuron(NeuralNetwork.max_neurons + o)

        sorted_genes = sorted(genome.genes, key=lambda g: g.output)
        for gene in sorted_genes:
            if gene.enabled:
                if gene.output not in self.neurons:
                    self.neurons[gene.output] = Neuron(gene.output)
                self.neurons[gene.output].incoming.append(gene)
                if gene.input not in self.neurons:
                    self.neurons[gene.input] = Neuron(gene.input)

    def evaluate(self, input_values):
        input_values.append(1)  # bias
        if len(input_values) != Genome.inputs or self.inputs != Genome.inputs:
            print('Zła ilość inputów')

        for i in range(len(input_values)):
            self.neurons[i].value = input_values[i]

        for neuron_id in self.neurons:
            inputs_sum = 0
            for incoming in self.neurons[neuron_id].incoming:
                inputs_sum += incoming.weight * self.neurons[incoming.input].value

            if inputs_sum > 0:
                self.neurons[neuron_id].value = steep_sigmoid(inputs_sum)

        output = []
        for i in range(self.outputs):
            if self.neurons[NeuralNetwork.max_neurons + i].value > 0.5:
                output.append(1)
            else:
                output.append(0)

        return output


def steep_sigmoid(x):
    weight = 4.9
    s = 1 / (1 + np.exp(-weight * x))

    return s
