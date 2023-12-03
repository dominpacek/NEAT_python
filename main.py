import time
import genetic_alg
from snake import play_game

if __name__ == "__main__":

    # Neural network parameters
    generations = 2000
    population_size = 100
    start = time.time()
    inputs = 5 + 1  # the 1 is for bias
    population = genetic_alg.generate_new_population(population_size, inputs, 3)
    i = 0
    best = 0
    #play_game(None, True, 5)
    while True:
        i += 1
        # Letting each genome play the game
        print()
        print(f'Generation {i}')
        max_score = 0
        best_genome_pop = population[0]
        avg = 0
        max_nodes = 0
        connections = 0
        for genome in population:
            genome_score, fitness = play_game(genome.nn, False, 50000, i)

            genome.fitness = fitness
            if genome_score > max_score:
                best_genome_pop = genome
                max_score = genome_score
                best = max(best, max_score)

            avg += genome_score
            max_nodes = max(max_nodes, len(genome.nn.neurons))
            connections = max(connections, len(genome.genes))

        avg = avg / len(population)
        end = time.time()
        print(f'took {(end - start):.2f} seconds')
        print(f'Best score: {max_score} (best ever {best})')
        print(f'Average score: {avg:.2f}')
        print(f'Max nodes: {max_nodes}')
        print(f'Max connections: {connections}')

        draw_graphs = False
        draw_every_n = 1
        if draw_graphs and i % draw_every_n == 0:
            best_genome_pop.nn.draw_graph()
            pass

        show_best = True
        if show_best:
            play_game(best_genome_pop.nn, False, 50, f"{i} (best)", (50, 50, 230))

        start = time.time()
        population = genetic_alg.next_generation(population)

    pygame.display.update()

    text = f'Final score: {genome_score}'
    display_text(text, 35, True, 500, 250)

    pygame.quit()
