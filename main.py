import numpy as np
import time
from ant_system import ant_system
from genetic_algorithm import genetic_algorithm
from matplotlib import pyplot as plt


def main():
    # reading data
    cities_file = np.loadtxt(r"Data\cities_4.txt").T

    # num of: ants/ cities
    k = cities_file.shape[0]
    # control parameters
    alpha = 1
    beta = 5
    # pheromone evaporation coefficient
    p = 0.5
    # number of iterations
    num_of_iter = 250

    start_as = time.time()
    best_score_as, best_path_as = ant_system(cities_file,
                                             k,
                                             num_of_iter,
                                             alpha,
                                             beta,
                                             p)
    end_as = time.time()
    print("Ant system \nscore: ", best_score_as, "\nbest path: ", best_path_as, "\ntime of execution: ",
          end_as - start_as)

    cities_as = np.ones((k+1, 2))*(-1)
    for idx, val in enumerate(best_path_as):
        cities_as[idx] = cities_file[val]

    # population size
    population_size = 250
    # parent to population population size ratio
    n = 0.8
    # probability of population element mutation
    mutation_probability = 0.2
    # number of iterations
    num_of_iter = 1000
    # algorithm used to select parents from population
    selection = "roulette_wheel"

    start_ga = time.time()
    best_score_ga, best_path_ga = genetic_algorithm(cities_file,
                                                    population_size,
                                                    num_of_iter,
                                                    n,
                                                    mutation_probability,
                                                    selection)
    end_ga = time.time()
    print("Genetic algorithm \nscore: ", best_score_ga, "\nbest path: ", best_path_ga, "\ntime of execution: ",
          end_ga - start_ga)
    cities_ga = np.ones((k+1, 2))*(-1)
    for idx, val in enumerate(best_path_ga):
        cities_ga[idx] = cities_file[val]

    fig, ax = plt.subplots(1, 2)
    ax[0].set_title("Path for Ant System")
    ax[1].set_title("Path for Genetic Algorithm")
    ax[0].plot(cities_as[:, 0], cities_as[:, 1])
    ax[0].scatter(cities_as[:, 0], cities_as[:, 1], c='r')
    ax[1].plot(cities_ga[:, 0], cities_ga[:, 1])
    ax[1].scatter(cities_ga[:, 0], cities_ga[:, 1], c='r')
    plt.show()


if __name__ == '__main__':
    main()
