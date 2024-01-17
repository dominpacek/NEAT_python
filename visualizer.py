import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import csv
from collections import defaultdict

def calculate_layer(edges):
    inputs = defaultdict(list)
    all_nodes = set()

    # Create the graph and collect all unique nodes
    for _,row in edges.iterrows():
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
        current_layer+=1
        unvisited_nodes = [n for n, is_visited in visited.items() if not is_visited]
        visited_nodes = [n for n, is_visited in visited.items() if is_visited]
        for node in unvisited_nodes:
            if set(visited_nodes).intersection(set(inputs[node])):
                visited[node] = True
                layers[node] = current_layer

    return layers

if __name__ == "__main__":
    graph_input = 'input/neat_connected_bestgenome.csv'
    with open(graph_input, 'r') as csv_file:
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
    plt.show()
