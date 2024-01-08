import time
from NEAT import neat_alg
from snake import play_game
from standard_genetic import genetic_alg


def play_game_with_standard(population_size, generations=-1):
    result_data = {'fields': ['generation', 'best_score', 'avg_score'],
                   'rows': []}

    start = time.time()
    inputs = 5 + 1  # 5 inputs + 1 bias
    population = genetic_alg.generate_new_population(population_size, inputs, 3, True)
    i = 0
    best = 0
    # play_game(None, True, 5)
    while i != generations:
        i += 1
        # Letting each genome play the game
        print()
        print(f'Generation {i}')
        max_score = 0
        best_genome_this_gen = population[0]
        avg = 0
        for genome in population:
            genome_score, fitness = play_game(genome.nn, False, 50000, i)

            genome.fitness = fitness
            if genome_score > max_score:
                best_genome_this_gen = genome
                max_score = genome_score
                best = max(best, max_score)

            avg += genome_score

        avg = avg / len(population)

        end = time.time()
        print(f'took {(end - start):.2f} seconds')
        print(
            f'Best score: {max_score} (best ever {best})')
        print(f'Average score: {avg:.2f}')

        show_best = False
        if show_best:
            play_game(best_genome_this_gen.nn, False, 50, f"{i} (best)", (50, 50, 230))

        result_data['rows'].append([i, max_score, avg])
        start = time.time()
        population = genetic_alg.next_generation(population)
    return result_data


def play_game_with_NEAT(population_size, generations=-1):
    result_data = {'fields': ['generation', 'best_score', 'avg_score', 'max_nodes', 'max_connections', 'species'],
                   'rows': []}

    start = time.time()
    inputs = 5 + 1  # 5 inputs + 1 bias
    population = neat_alg.generate_new_population(population_size, inputs, 3, True)
    i = 0
    best = 0
    best_genome = population[0]
    # play_game(None, True, 5)
    while i != generations:
        i += 1
        # Letting each genome play the game
        print()
        print(f'Generation {i}')
        max_score = 0
        best_genome_this_gen = population[0]
        avg = 0
        max_nodes = 0
        connections = 0
        species = {}
        for genome in population:
            genome_score, fitness = play_game(genome.nn, False, 50000, i)

            genome.fitness = fitness
            if genome_score > max_score:
                best_genome_this_gen = genome
                max_score = genome_score
                best = max(best, max_score)
                best_genome = genome

            avg += genome_score
            max_nodes = max(max_nodes, len(genome.nn.neurons))
            connections = max(connections, len(genome.connection_genes))
            if genome.species in species:
                species[genome.species] += 1
            else:
                species[genome.species] = 1

        avg = avg / len(population)
        end = time.time()
        print(f'took {(end - start):.2f} seconds')
        print(
            f'Best score: {max_score} ({len(best_genome_this_gen.nn.neurons)}n, {len(best_genome_this_gen.connection_genes)}c) (best ever {best})')
        print(f'Average score: {avg:.2f}')
        # print(f'Max nodes: {max_nodes}')
        # print(f'Max connections: {connections}')
        print(f'Species: {species}')

        draw_graphs = False
        draw_every_n = 1
        if draw_graphs and i % draw_every_n == 0:
            best_genome_this_gen.nn.draw_graph()
            pass

        show_best = False
        if show_best:
            play_game(best_genome_this_gen.nn, False, 50, f"{i} (best)", (50, 50, 230))
        result_data['rows'].append([i, max_score, avg, max_nodes, connections, species])
        start = time.time()
        population = neat_alg.next_generation(population)

    best_genome.nn.draw_graph()

    return result_data
