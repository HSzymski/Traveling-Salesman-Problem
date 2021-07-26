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

    list_parents = []
    for i in range(num_of_iter):
        if len(list_parents) != 0:
            list_parents = evaluate_cost(list_parents, cities)
        # make list of parents of size n time population size
        list_parents = roulette_wheel_algorithm(list_population, n)

        list_offsprings = create_offsprings()

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


def evaluate_cost(list_population: list, cities: np.array) -> list:
    for population_element in list_population:
        for list_idx in range(1,len(population_element["parent_idx"])):
            actual_city = cities[population_element["parent_idx"][list_idx]]
            previous_city = cities[population_element["parent_idx"][list_idx-1]]
            population_element["dist_traveled"] += distance.euclidean(actual_city,previous_city)
    return list_population


def roulette_wheel_algorithm(list_population: list, n: float) -> list:
    sum_of_dist = sum([population_element['dist_traveled'] for population_element in list_population])
    relative_probabilities = [population_element['dist_traveled']/sum_of_dist for population_element in list_population]
    cumulative_probabilities = [sum(relative_probabilities[:i+1]) for i in range(len(relative_probabilities))]

    list_parents = []
    while (len(list_parents) < n*len(list_population)):
        rand = random.uniform(0,1)

        idx = 0
        while(cumulative_probabilities[idx] < rand):
            idx += 1
        list_parents.append(list_population[idx])
    return list_parents


def mutation():
    pass


def create_offsprings():
    rand_idx_1 = random.uniform(0,1)
    rand_idx_2 = random.uniform(0,1)
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
