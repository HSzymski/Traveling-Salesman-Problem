import numpy as np
import time
from ant_system import ant_system
from genetic_algorithm import genetic_algorithm
from simulated_annealing import simulated_annealing
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator


def main():
    # reading data
    cities_file = np.loadtxt(r'Data\cities_4.txt').T

    # Parameters for Ant system
    # num of: ants/ cities
    k = cities_file.shape[0]
    # control parameters
    alpha = 1
    beta = 5
    # pheromone evaporation coefficient
    p = 0.5
    # number of iterations
    num_of_iter = 250
    tuple_parameters_as = tuple((cities_file,
                                 k,
                                 num_of_iter,
                                 alpha,
                                 beta,
                                 p))

    # Parameters for Genetic algorithm
    # population size
    population_size = 250
    # parent to population population size ratio
    n = 0.8
    # probability of population element mutation
    mutation_probability = 0.2
    # number of iterations
    num_of_iter = 1000
    # algorithm used to select parents from population
    selection = 'roulette_wheel'
    tuple_parameters_ga = tuple((cities_file,
                                 population_size,
                                 num_of_iter,
                                 n,
                                 mutation_probability,
                                 selection))

    # Parameters for Simulated annealing
    # starting temperature
    initial_temperature = 10 * 6
    # temperature used as loop stop condition
    minimum_temperature = 0.01
    # parameter for scheduling
    alpha = 0.998
    # scheduling type
    scheduling = 'inverse'  # 'exponential'
    tuple_parameters_sa = tuple((cities_file,
                                 initial_temperature,
                                 minimum_temperature,
                                 alpha,
                                 scheduling))

    algorithms_runs = 30
    list_results_as = np.zeros((algorithms_runs, 2))
    list_results_ga = np.zeros((algorithms_runs, 2))
    list_results_sa = np.zeros((algorithms_runs, 2))
    for iteration in range(algorithms_runs):
        start_as = time.time()
        best_score_as, best_path_as = ant_system(*tuple_parameters_as)
        end_as = time.time()
        list_results_as[iteration] = [best_score_as, end_as - start_as]

        start_ga = time.time()
        best_score_ga, best_path_ga = genetic_algorithm(*tuple_parameters_ga)
        end_ga = time.time()
        list_results_ga[iteration] = [best_score_ga, end_ga - start_ga]

        start_sa = time.time()
        best_score_sa, best_path_sa = simulated_annealing(*tuple_parameters_sa)
        end_sa = time.time()
        list_results_sa[iteration] = [best_score_sa, end_sa - start_sa]

    list_iter_numbers = [i for i in range(1, algorithms_runs + 1)]

    fig, ax = plt.subplots(2, 1, figsize=(12, 6))
    fig.tight_layout(pad=2.0)
    ax[0].set_title('Best scores of each algorithm')
    ax[0].plot(list_iter_numbers, list_results_as[:, 0], label='Ant system')
    ax[0].plot(list_iter_numbers, list_results_ga[:, 0], label='Genetic algorithm')
    ax[0].plot(list_iter_numbers, list_results_sa[:, 0], label='Simulated annealing')
    ax[0].xaxis.set_major_locator(MultipleLocator(1))
    ax[0].legend(loc='upper right')
    ax[0].set_xlabel('Iteration number')
    ax[0].set_ylabel('Best score')

    ax[1].set_title('Times of execution of each algorithm')
    ax[1].plot(list_iter_numbers, list_results_as[:, 1], label='Ant system')
    ax[1].plot(list_iter_numbers, list_results_ga[:, 1], label='Genetic algorithm')
    ax[1].plot(list_iter_numbers, list_results_sa[:, 1], label='Simulated annealing')
    ax[1].xaxis.set_major_locator(MultipleLocator(1))
    ax[1].legend(loc='upper right')
    ax[1].set_xlabel('Iteration number')
    ax[1].set_ylabel('Best score')
    plt.show()

    fig.savefig('results.png')

    with open('results.txt', 'w') as f:
        f.writelines(['Mean best distances:\n',
                      f'Ant system: {sum(list_results_as[:, 0]) / len(list_results_as[:, 0])}\n',
                      f'Genetic algorithm: {sum(list_results_ga[:, 0]) / len(list_results_as[:, 0])}\n',
                      f'Simulated annealing: {sum(list_results_sa[:, 0]) / len(list_results_as[:, 0])}\n',
                      'Mean times:\n',
                      f'Ant system: {sum(list_results_as[:, 1]) / len(list_results_as[:, 1])}\n',
                      f'Genetic algorithm: {sum(list_results_ga[:, 1]) / len(list_results_as[:, 1])}\n',
                      f'Simulated annealing: {sum(list_results_sa[:, 1]) / len(list_results_as[:, 1])}\n'])


if __name__ == '__main__':
    main()
