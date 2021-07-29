import numpy as np
from ant_system import ant_system
from genetic_algorithm import genetic_algorithm


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
    num_of_iter = 200

    best_score, best_path = ant_system(cities_file,
                                       k,
                                       num_of_iter,
                                       alpha,
                                       beta,
                                       p)
    print("Ant system: ", best_score, best_path)

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

    best_score, best_path = genetic_algorithm(cities_file,
                                              population_size,
                                              num_of_iter,
                                              n,
                                              mutation_probability,
                                              selection)
    print("Genetic algorithm: ", best_score, best_path)


if __name__ == '__main__':
    main()
