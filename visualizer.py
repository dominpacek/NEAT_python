import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import csv
from collections import defaultdict
from datetime import datetime


def calculate_layer(edges):
    inputs = defaultdict(list)
    all_nodes = set()

    # Create the graph and collect all unique nodes
    for _, row in edges.iterrows():
        input_node = row['input']
        output_node = row['output']
        inputs[output_node].append(input_node)
        all_nodes.add(input_node)
        all_nodes.add(output_node)

    visited = {node: False for node in all_nodes}
    layers = {node: 0 for node in all_nodes}
    current_layer = 0

    for node in all_nodes:
        if not inputs[node]:
            visited[node] = True
            layers[node] = current_layer
    while not all(visited.values()):
        current_layer += 1
        unvisited_nodes = [n for n, is_visited in visited.items() if not is_visited]
        visited_nodes = [n for n, is_visited in visited.items() if is_visited]
        for node in unvisited_nodes:
            if set(visited_nodes).intersection(set(inputs[node])):
                visited[node] = True
                layers[node] = current_layer

    return layers


def draw_network_graph(filename):
    with open(filename, 'r') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file, ['input', 'output', 'weight'])

        data = {
            'input': [],
            'output': [],
            'weight': []
        }

        # Skip the first 3 rows
        for _ in range(3):
            next(csv_reader)
        for row in csv_reader:
            if not row:
                continue
            data['input'].append(int(row['input']))
            data['output'].append(int(row['output']))
            data['weight'].append(float(row['weight']))

    df = pd.DataFrame(data)
    df.sort_values(by=['input', 'output'], inplace=True)
    layers_subset = calculate_layer(df)

    G = nx.from_pandas_edgelist(df, 'input', 'output', 'weight', create_using=nx.DiGraph())

    for node in G.nodes:
        if node > 100000:
            G.nodes[node]['layer'] = 9999
        else:
            G.nodes[node]['layer'] = layers_subset[node]

    # Create a mapping for renaming nodes
    rename_mapping = {0: 'i1',
                      1: 'i2',
                      2: 'i3',
                      3: 'i4',
                      4: 'i5',
                      5: 'i6',
                      1000000: 'o1',
                      1000001: 'o2',
                      1000002: 'o3'}
    # Rename nodes using the mapping
    G = nx.relabel_nodes(G, rename_mapping)

    pos = nx.multipartite_layout(G, subset_key="layer", align='vertical')
    nx.draw(G, pos, with_labels=False, node_color='green', arrows=True, arrowstyle='->', arrowsize=10,
            font_color='white', font_size=10, edge_color='#535353')
    plt.savefig(f'output/{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}_genome.pdf', format='pdf')
    plt.show()


def plot_generations_old(save_plot=True):
    # method to plot comparison of best and average scores of the tree approaches
    # (old method with hardcoded names)
    with open('output/neat_connected.csv', 'r') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file, ['generation', 'best_score', 'avg_score'], lineterminator='\n')

        # Skip the first 3 rows
        for _ in range(3):
            next(csv_reader)
        neatc_generations = []
        neatc_best_scores = []
        neatc_avg_scores = []
        for row in csv_reader:
            if not row:
                continue
            neatc_generations.append(int(row['generation']))
            neatc_best_scores.append(float(row['best_score']))
            neatc_avg_scores.append(float(row['avg_score']))
            # print(row)

    with open('output/neat_disconnected.csv', 'r') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file, ['generation', 'best_score', 'avg_score'], lineterminator='\n')

        # Skip the first 3 rows
        for _ in range(3):
            next(csv_reader)
        neatd_generations = []
        neatd_best_scores = []
        neatd_avg_scores = []
        for row in csv_reader:
            if not row:
                continue
            neatd_generations.append(int(row['generation']))
            neatd_best_scores.append(float(row['best_score']))
            neatd_avg_scores.append(float(row['avg_score']))
            # print(row)

    with open('output/standard.csv', 'r') as csv_file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(csv_file, ['generation', 'best_score', 'avg_score'], lineterminator='\n')

        # Skip the first 3 rows
        for _ in range(3):
            next(csv_reader)
        standard_generations = []
        standard_best_scores = []
        standard_avg_scores = []
        for row in csv_reader:
            if not row:
                continue
            standard_generations.append(int(row['generation']))
            standard_best_scores.append(float(row['best_score']))
            standard_avg_scores.append(float(row['avg_score']))
            # print(row)

    # Plot the functions with axes
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Uzyskane wyniki na przebiegu pokoleń')

    ax[0].plot(standard_generations, standard_best_scores, label='Proste podejście', linewidth=1)
    ax[0].plot(neatc_generations, neatc_best_scores, label='NEAT z połączeniami', linewidth=1.25, linestyle='solid')
    ax[0].plot(neatd_generations, neatd_best_scores, label='NEAT bez połączeń', linewidth=1)
    # ax[0].legend(loc='lower right')
    ax[0].title.set_text('Najlepszy osobnik')
    ax[0].set_ylabel('Zjedzone jabłka')

    ax[1].plot(standard_generations, standard_avg_scores, label='Proste podejście', linewidth=1)
    ax[1].plot(neatc_generations, neatc_avg_scores, label='NEAT z połączeniami', linewidth=1)
    ax[1].plot(neatd_generations, neatd_avg_scores, label='NEAT bez połączeń', linewidth=1)
    # ax[1].legend(loc='upper right')
    ax[1].title.set_text('Średnia populacji')
    fig.legend(*ax[1].get_legend_handles_labels(),
               loc='lower center', ncol=4)

    # fig.tight_layout()
    ax[0].set_xlim([1, len(neatc_generations) + 5])
    ax[0].set_ylim([0, max(neatd_best_scores)])
    ax[1].set_xlim([1, len(neatc_generations) + 5])
    ax[1].set_ylim([0, max(neatd_avg_scores)])
    # ax.set_xlabel('x')
    # ax.set_ylabel('Function Value')
    # ax.set_title('Activation Functions: ReLU, Sigmoid, Tanh')
    if save_plot:
        plt.savefig('output/generations-plot.pdf', format='pdf')
    plt.show()


def plot_generations(file_names, save_plot=True, plot_output="output-plot.pdf", show_plot=True):
    # method to plot comparison of best and average scores of the tree approaches
    # (currently the filenames are hardcoded)
    data = {}
    highest_generation = 1
    max_best = 1
    max_avg = 1

    for file in file_names:
        with open(f'output/{file}', 'r') as csv_file:
            # Create a CSV reader object
            csv_reader = csv.DictReader(csv_file, ['generation', 'best_score', 'avg_score'], lineterminator='\n')

            # Skip the first 3 rows with additional info
            for _ in range(3):
                next(csv_reader)
            data[file] = {'generations': [],
                          'best_scores': [],
                          'avg_scores': []}

            for row in csv_reader:
                if not row:
                    # skip empty rows
                    continue
                gen = int(row['generation'])
                best_score = int(row['best_score'])
                avg_score = float(row['avg_score'])

                highest_generation = max(highest_generation, gen)
                max_best = max(max_best, best_score)
                max_avg = max(max_avg, avg_score)

                data[file]['generations'].append(gen)
                data[file]['best_scores'].append(best_score)
                data[file]['avg_scores'].append(avg_score)

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Uzyskane wyniki na przebiegu pokoleń')

    ax[0].set_ylabel('Zjedzone jabłka')

    ax[0].title.set_text('Najlepszy osobnik')
    ax[1].title.set_text('Średnia populacji')

    for file in file_names:
        ax[0].plot(data[file]['generations'], data[file]['best_scores'], label=file, linewidth=1)

        ax[1].plot(data[file]['generations'], data[file]['avg_scores'], label=file, linewidth=1)

    fig.legend(*ax[0].get_legend_handles_labels(),
               loc='lower center', ncol=4)

    # fig.tight_layout()
    ax[0].set_xlim([1, highest_generation + 5])
    ax[0].set_ylim([0, max_best])
    ax[1].set_xlim([1, highest_generation + 5])
    ax[1].set_ylim([0, max_avg])

    if save_plot:
        plt.savefig(f"output/{plot_output}", format='pdf')
    if show_plot:
        plt.show()
    plt.close()


if __name__ == "__main__":
    graph_input = 'input/neat_disconnected_bestgenome.csv'
    draw_network_graph(graph_input)
