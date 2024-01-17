from startup import *
import csv

# Neural network parameters
generations = 250
population_size = 200


def save_results(file_name, fields, rows):
    with open('output/' + file_name, 'w') as f:
        writer = csv.writer(f)

        writer.writerow(["Generations", generations])
        writer.writerow(["Population size", population_size])

        writer.writerow(fields)
        writer.writerows(rows)


if __name__ == "__main__":
    # results_std = play_game_with_standard(population_size, generations)
    # save_results("standard.csv", results_std['fields'], results_std['rows'])
    results_neat_connected = play_game_with_NEAT(population_size, generations)

    # todo fix the line endings, and make a separate class for the save_results function
    results_neat_disconnected = play_game_with_NEAT(population_size, generations, False)

    save_results("neat_connected.csv", results_neat_connected['fields'], results_neat_connected['rows'])
    genome_data = results_neat_connected['best_genome'].generate_graph_data()
    save_results("neat_connected_bestgenome.csv", genome_data['fields'], genome_data['rows'])

    save_results("neat_disconnected.csv", results_neat_disconnected['fields'], results_neat_disconnected['rows'])
    genome_data = results_neat_disconnected['best_genome'].generate_graph_data()
    save_results("neat_disconnected_bestgenome.csv", genome_data['fields'], genome_data['rows'])
