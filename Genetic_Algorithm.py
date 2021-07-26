import numpy as np
import random
from scipy.spatial import distance


def genetic_algorithm(cities: np.array,
                      population_size: int,
                      num_of_iter: int,
                      n: float,
                      mutation_probability: float) -> int:
    num_of_cities = cities.shape[0]
    #array_dist_between_cities = calc_distance_array(cities)

    list_population = create_initial_population(population_size, num_of_cities)
    list_population = evaluate_cost(list_population, cities)

    while i in range(num_of_iter):
        create_parent_population()

        offspring_array_size = 0
        while offspring_array_size == n*p:
            create_offspring()


        create_parent_population()

    pass


def create_initial_population(population_size: int, num_of_cities) -> list:
    list_population = []

    # for each parent in population create list of indexes and
    # calculate total distance traveled (cost) equal to 0
    for i in range(population_size):
        list_of_cities_idx = [idx for idx in range(num_of_cities)]
        # (shuffle method works in place and returns nothing)
        random.shuffle(list_of_cities_idx)

        # add idx of the first city
        list_of_cities_idx.append(list_of_cities_idx[0])
        list_population.append({"parent_idx": list_of_cities_idx, "dist_traveled": 0})
    return list_population


def evaluate_cost(list_parents: list, cities: np.array) -> list:
    for parents in list_parents:
        for list_idx in range(1,len(parents["parent_idx"])):
            actual_city = cities[parents["parent_idx"][list_idx]]
            previous_city = cities[parents["parent_idx"][list_idx-1]]
            parents["dist_traveled"] += distance.euclidean(actual_city,previous_city)
    return list_parents


def mutation():
    pass


def create_offspring():
    mutation()
    pass


def main():
    # reading data
    cities_file = np.loadtxt("Data\cities_4.txt").T

    # population size
    population_size = 250
    # parent to population population size ratio
    n = 0.8
    # probability of mutation
    mutation_probability = 0.2
    # number of iterations
    num_of_iter = 1000

    best_score = genetic_algorithm(cities_file, population_size, num_of_iter, n , mutation_probability)
    print(best_score)

if __name__ == '__main__':
    main()
