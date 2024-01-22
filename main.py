from startup import *
from result_logger import save_results_to_csv
from visualizer import plot_generations
import NEAT.neat_parameters as params

# Neural network parameters
generations = 3
population_size = 20

if __name__ == "__main__":
    files = []
    params.crossover_rate = 0

    # zmiany parametru krzyżowania
    results = play_game_with_NEAT(population_size, generations, True)
    file = "neat_no_crossover.csv"
    save_results_to_csv(file, results, generations, population_size)
    files.append(file)

    params.crossover_rate = 0.5
    results = play_game_with_NEAT(population_size, generations, True)
    file = "neat_50_crossover.csv"
    save_results_to_csv(file, results, generations, population_size)
    files.append(file)

    params.crossover_rate = 0.8
    results = play_game_with_NEAT(population_size, generations, True)
    file = "neat_80_crossover.csv"
    save_results_to_csv(file, results, generations, population_size)
    files.append(file)

    params.crossover_rate = 1
    results = play_game_with_NEAT(population_size, generations, True)
    file = "neat_100_crossover.csv"
    save_results_to_csv(file, results, generations, population_size)
    files.append(file)

    plot_generations(file_names=files, save_plot=True, show_plot=True)

    # zmiany parametru mutacji
    params.crossover_rate = 0.8
    files = []

    params.connection_mutation_rate = 0
    params.node_mutation_rate = 0
    params.weight_mutation_rate = 0
    results = play_game_with_NEAT(population_size, generations, True)
    file = "neat_no_mutation.csv"
    save_results_to_csv(file, results, generations, population_size)
    files.append(file)

    params.connection_mutation_rate = 0.05
    params.node_mutation_rate = 0.05
    params.weight_mutation_rate = 0.05
    file = "neat_low_mutation.csv"
    results = play_game_with_NEAT(population_size, generations, True)
    save_results_to_csv(file, results, generations, population_size)
    files.append(file)

    params.connection_mutation_rate = 0.3
    params.node_mutation_rate = 0.1
    params.weight_mutation_rate = 0.4
    file = "neat_medium_mutation.csv"
    results = play_game_with_NEAT(population_size, generations, True)
    save_results_to_csv(file, results, generations, population_size)
    files.append(file)

    params.connection_mutation_rate = 0.5
    params.node_mutation_rate = 0.2
    params.weight_mutation_rate = 0.7
    file = "neat_high_mutation.csv"
    results = play_game_with_NEAT(population_size, generations, True)
    save_results_to_csv(file, results, generations, population_size)
    files.append(file)

    plot_generations(file_names=files, save_plot=True, show_plot=True)

    # genome_data = results_neat_connected['best_genome'].generate_network_graph_data()
    # save_results_to_csv("neat_connected_bestgenome.csv", genome_data, generations, population_size)

