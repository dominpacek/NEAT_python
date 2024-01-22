import csv


def save_results_to_csv(file_name, data, generations, population_size):
    with open('output/' + file_name, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')

        writer.writerow(["Generations", generations])
        writer.writerow(["Population size", population_size])

        writer.writerow(data['fields'])
        writer.writerows(data['rows'])
