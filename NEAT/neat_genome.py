import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class NeatGenome:
    input_count = -1
    output_count = -1
    _Neuron_innovation = -1

    def __init__(self, input_count, output_count):
        self.input_count = input_count
        self.output_count = output_count
        self.species = 0  # TODO

        self.connection_genes = []
        NeatGenome._Neuron_innovation = input_count - 1
        self.nn = None
        if NeatGenome.input_count == -1:
            NeatGenome.input_count = input_count
        elif NeatGenome.input_count != input_count:
            print('Zła ilość inputów w genomie')
        if NeatGenome.output_count == -1:
            NeatGenome.output_count = output_count
        elif NeatGenome.output_count != output_count:
            print('Zła ilość outputów w genomie')

    def add_connection(self, gene):
        self.connection_genes.append(gene)

    def get_new_neuron_id(self):
        NeatGenome._Neuron_innovation += 1
        return NeatGenome._Neuron_innovation

    def random_neuron(self, inputs_allowed=False, outputs_allowed=False):
        neurons = {}
        if inputs_allowed:
            for i in range(self.input_count):
                neurons[i] = True
        if outputs_allowed:
            for o in range(self.output_count):
                neurons[NeuralNetwork.max_neurons + o] = True
        for gene in self.connection_genes:
            if self.input_count <= gene.input < NeuralNetwork.max_neurons:
                neurons[gene.input] = True
            if self.input_count <= gene.output < NeuralNetwork.max_neurons:
                neurons[gene.output] = True

        # Error checking
        for i in list(neurons.keys()):
            if not inputs_allowed:
                if i < self.input_count:
                    print("Error: random_neuron returned INPUT when not allowed")
            if not outputs_allowed:
                if i >= NeuralNetwork.max_neurons:
                    print("Error: random_neuron returned OUTPUT when not allowed")

        neuron = np.random.choice(list(neurons.keys()))
        return neuron

    def generate_nn(self):
        self.nn = NeuralNetwork(self)

    def already_has_gene(self, input, output):
        for gene in self.connection_genes:
            if gene.input == input and gene.output == output:
                return True
        return False


# class NodeType(Enum):
#     INPUT = 0
#     OUTPUT = 1
#     HIDDEN = 2
#
#
# class NodeGene:
#     _Innovation = 0
#
#     def __init__(self, node_type=NodeType.HIDDEN, innovation=None):
#         self.type = node_type
#         if innovation is not None:
#             self.innovation = innovation
#         else:
#             NodeGene._Innovation += 1
#             self.innovation = NodeGene._Innovation


class ConnectionGene:
    _Innovation = 0

    def __init__(self, input, output, weight=random.uniform(-1, 1), enabled=True, innovation=None):
        if input == output:
            print('Error: self loop connection')
        self.input = input
        self.output = output
        self.weight = weight
        self.enabled = enabled
        if innovation is not None:
            self.innovation = innovation
        else:
            ConnectionGene._Innovation += 1
            self.innovation = ConnectionGene._Innovation


class NN_Neuron:

    def __init__(self, neuron_id):
        self.value = 0
        self.id = neuron_id
        self.incoming = []


class NeuralNetwork:
    max_neurons = 1000000

    def __init__(self, genome):
        self.neurons = {}
        self.inputs = genome.input_count
        self.outputs = genome.output_count

        for i in range(genome.input_count):
            self.neurons[i] = NN_Neuron(i)
        for o in range(genome.output_count):
            self.neurons[NeuralNetwork.max_neurons + o] = NN_Neuron(NeuralNetwork.max_neurons + o)

        sorted_genes = sorted(genome.connection_genes, key=lambda g: g.output)
        for gene in sorted_genes:
            if gene.input > NeuralNetwork.max_neurons:
                print('Error: Output acting as input')
            if gene.enabled:
                if gene.output not in self.neurons:
                    self.neurons[gene.output] = NN_Neuron(gene.output)
                self.neurons[gene.output].incoming.append(gene)
                if gene.input not in self.neurons:
                    self.neurons[gene.input] = NN_Neuron(gene.input)

    def evaluate(self, input_values):
        input_values.append(1)  # bias
        if len(input_values) != NeatGenome.input_count or self.inputs != NeatGenome.input_count:
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

        return output

    def draw_graph(self):
        plt.clf()
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
