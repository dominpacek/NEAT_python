import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class Genome:
    inputs = -1
    outputs = -1

    def __init__(self, inputs, outputs, neuron_count=None):
        # inputs and outputs are ints
        self.inputs = inputs
        self.outputs = outputs
        if neuron_count is None:
            self.neuron_count = inputs
        else:
            self.neuron_count = neuron_count
        self.genes = []
        self.nn = None
        if Genome.inputs == -1:
            Genome.inputs = inputs
        elif Genome.inputs != inputs:
            print('Zła ilość inputów w genomie')
        if Genome.outputs == -1:
            Genome.outputs = outputs
        elif Genome.outputs != outputs:
            print('Zła ilość outputów w genomie')

    def add_gene(self, gene):
        if gene.input >= self.neuron_count or (self.neuron_count <= gene.output < NeuralNetwork.max_neurons):
            print('Error: gene input or output out of range')
            print(f'    input: {gene.input}, output: {gene.output}, neuron_count: {self.neuron_count}')
        self.genes.append(gene)

    def get_new_neuron_id(self):
        self.neuron_count += 1
        return self.neuron_count - 1

    def random_neuron(self, inputs_allowed=False, outputs_allowed=False):
        neurons = {}
        if inputs_allowed:
            for i in range(self.inputs):
                neurons[i] = True
        if outputs_allowed:
            for o in range(self.outputs):
                neurons[NeuralNetwork.max_neurons + o] = True
        for gene in self.genes:
            if self.inputs <= gene.input < NeuralNetwork.max_neurons:
                neurons[gene.input] = True
            if self.inputs <= gene.output < NeuralNetwork.max_neurons:
                neurons[gene.output] = True

        # Error checking
        for i in list(neurons.keys()):
            if not inputs_allowed:
                if i < self.inputs:
                    print("Error: random_neuron returned INPUT when not allowed")
            if not outputs_allowed:
                if i >= NeuralNetwork.max_neurons:
                    print("Error: random_neuron returned OUTPUT when not allowed")

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
    def __init__(self, neuron_id):
        self.value = 0
        self.id = neuron_id
        self.incoming = []
        # TODO add layer info


class Gene:
    _Innovation = 0

    def __init__(self, input, output, weight=random.random(), increase_innovation=True, enabled=True):
        if input == output:
            print('Error: self loop connection')
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
            if gene.input > NeuralNetwork.max_neurons:
                print('Error: Output acting as input')
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

            if len(self.neurons[neuron_id].incoming):
                self.neurons[neuron_id].value = steep_sigmoid(inputs_sum)

        output = []
        for i in range(self.outputs):
            output.append(self.neurons[NeuralNetwork.max_neurons + i].value)
            # if self.neurons[NeuralNetwork.max_neurons + i].value > 0.5:
            #     output.append(1)
            # else:
            #     output.append(0)

        return output

    def draw_graph(self):
        G = nx.DiGraph()

        input_neurons = [neuron_id for neuron_id in self.neurons if neuron_id < self.inputs]
        output_neurons = [neuron_id for neuron_id in self.neurons if neuron_id >= NeuralNetwork.max_neurons]

        for neuron_id in input_neurons:
            G.add_node(neuron_id, pos=(0, neuron_id), label=str(neuron_id))

        for neuron_id in output_neurons:
            node_label = f"{neuron_id}\nValue: {self.neurons[neuron_id].value:.2f}"
            G.add_node(neuron_id, pos=(2, neuron_id - NeuralNetwork.max_neurons))
            G.nodes[neuron_id]['label'] = node_label

        for neuron_id, neuron in self.neurons.items():
            if neuron_id not in input_neurons and neuron_id not in output_neurons:
                G.add_node(neuron_id, pos=(1, neuron_id), label=str(neuron_id))

        for neuron_id, neuron in self.neurons.items():
            for gene in neuron.incoming:
                edge_color = 'black' if gene.enabled else 'gray'
                G.add_edge(gene.input, gene.output, label=f"{gene.weight:.2f}", color=edge_color)

        pos = nx.get_node_attributes(G, 'pos')
        node_labels = {node: data['label'] for node, data in G.nodes(data=True)}
        edge_colors = nx.get_edge_attributes(G, 'color')
        labels = nx.get_edge_attributes(G, 'label')

        edge_color_list = [edge_colors[edge] for edge in G.edges()]
        nx.draw(G, pos, with_labels=False, node_size=500, node_color='skyblue', font_size=8, edge_color=edge_color_list)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red', font_size=8)
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, verticalalignment="center",
                                horizontalalignment="left")

        plt.show(block=False)
        plt.pause(0.0001)


def steep_sigmoid(x):
    weight = 4.9
    s = 1 / (1 + np.exp(-weight * x))

    return s
