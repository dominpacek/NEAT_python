from startup import *
import csv

# Neural network parameters
generations = 250
population_size = 200


def save_results(file_name, fields, rows):
    with open('output/' + file_name, 'w') as f:
        # using csv.writer method from CSV package
        writer = csv.writer(f)

        writer.writerow(["Generations", generations])
        writer.writerow(["Population size", population_size])

        writer.writerow(fields)
        writer.writerows(rows)


if __name__ == "__main__":
    results_std = play_game_with_standard(population_size, generations)
    save_results("standard.csv", results_std['fields'], results_std['rows'])

    results_neat = play_game_with_NEAT(population_size, generations)
    save_results("neat.csv", results_neat['fields'], results_neat['rows'])

    input("Press Enter to continue...")