import numpy as np
import random
from scipy.spatial import distance
from typing import List


def genetic_algorithm(cities: np.array,
                      population_size: int,
                      num_of_iter: int,
                      n: float,
                      mutation_probability: float,
                      selection: str) -> int:
    num_of_cities = cities.shape[0]

    # create initial population of population_size pahts
    list_population = create_initial_population(population_size, num_of_cities)
    # evaluate cost for whole population
    list_population = evaluate_cost(list_population, cities)
    if selection == "kbest":
        list_population = sorted(list_population, key=lambda population_element: population_element['dist_traveled'])

    for i in range(num_of_iter):
        # make list of parents of size n times population size by different types of selection
        if selection == "roulette_wheel":
            list_parents = roulette_wheel_algorithm(list_population, population_size, n)
        elif selection == "kbest":
            list_parents = list_population[:population_size]
        # create offsprings and perform cycle crossover with mutation on them
        list_offsprings = create_offsprings(list_parents, mutation_probability)
        # evaluate distances
        list_offsprings = evaluate_cost(list_offsprings, cities)
        # concatenate parents and offsprings to create new population, then sort them by distances
        list_population = list_parents + list_offsprings
        list_population = sorted(list_population, key=lambda population_element: population_element['dist_traveled'])
        print("Iteration number: ",i)
    best_score = list_population[0]['dist_traveled']
    return best_score


def create_initial_population(population_size: int, num_of_cities) -> List[dict]:
    list_population = []
    # for each parent in population create list of indexes and
    # calculate total distance traveled (cost) equal to 0
    for i in range(population_size):
        list_of_cities_idx = [idx for idx in range(num_of_cities)]
        # (shuffle method works in place and returns nothing)
        random.shuffle(list_of_cities_idx)

        # add idx of the first city
        list_of_cities_idx.append(list_of_cities_idx[0])
        list_population.append({'parent_idx': list_of_cities_idx, 'dist_traveled': 0})
    return list_population


def evaluate_cost(list_population: List[dict], cities: np.array) -> List[dict]:
    for population_element in list_population:
        for list_idx in range(1,len(population_element['parent_idx'])):
            actual_city = cities[population_element['parent_idx'][list_idx]]
            previous_city = cities[population_element['parent_idx'][list_idx-1]]
            population_element['dist_traveled'] += distance.euclidean(actual_city,previous_city)
    return list_population


def roulette_wheel_algorithm(list_population: List[dict], population_size: int, n: float) -> List[dict]:
    # checking maximum value of dist_traveled to scale date for calculating probabilities
    max_list_val = 0
    for population_element in list_population:
        if population_element['dist_traveled'] > max_list_val:
            max_list_val = population_element['dist_traveled']
    # calculating sum of distances
    sum_of_dist = sum([max_list_val-population_element['dist_traveled'] for population_element in list_population])
    # relative probabilities for each element of population
    relative_probabilities = [(max_list_val-population_element['dist_traveled'])/sum_of_dist for population_element in list_population]
    # cumulative probabilities for each element of population
    cumulative_probabilities = [sum(relative_probabilities[:i+1]) for i in range(len(relative_probabilities))]
    list_parents = []
    # selection loop
    while (len(list_parents) < n*population_size):
        rand = random.uniform(0,1)
        idx = 0
        while(cumulative_probabilities[idx] < rand):
            idx += 1
        list_parents.append(list_population[idx])
    return list_parents


def create_offsprings(list_parents: List[dict], mutation_probability: float) -> list:
    list_offspring = []
    while len(list_offspring) != len(list_parents):
        rand_parent_1 = random.choice(list_parents)
        rand_parent_2 = random.choice(list_parents)

        offspring_1 = cycle_crossover_with_mutation(rand_parent_1['parent_idx'],
                                                    rand_parent_2['parent_idx'],
                                                    mutation_probability)
        offspring_2 = cycle_crossover_with_mutation(rand_parent_2['parent_idx'],
                                                    rand_parent_1['parent_idx'],
                                                    mutation_probability)

        list_offspring.append({'parent_idx': offspring_1,'dist_traveled':0})
        list_offspring.append({'parent_idx': offspring_2,'dist_traveled':0})
    return list_offspring

def cycle_crossover_with_mutation(parent_idx_1: list, parent_idx_2: list, mutation_probability: float) -> list:
    parent_without_return_1 = parent_idx_1[:-1]
    parent_without_return_2 = parent_idx_2[:-1]
    offspring = [-1 for i in range(len(parent_without_return_1))]
    # Cycle crossover realized in 5 steps
    # 1. start with the frst unused position of O and the frst allele of P1
    offspring[0] = parent_without_return_1[0]
    # 2. look at the allele in the same position in P2
    value_to_find = parent_without_return_2[0]
    for i in range(len(offspring)-1): # maximum possible number of iteration
        # 3. go to the position with the same allele in P1
        value_idx = parent_without_return_1.index(value_to_find)
        # 4. add this allele into cycle
        offspring[value_idx] = value_to_find
        # 5. repeat steps 2 through 4 until arrive at the frst allele of P1
        value_to_find = parent_without_return_2[value_idx]
        if value_to_find in offspring:
            break
    # fill other city indexes using second parent indexes
    for idx, val in enumerate(offspring):
        if val == -1:
            offspring[idx] = parent_without_return_2[idx]
    # check for mutation
    offspring = mutation(offspring, mutation_probability)
    # append starting point
    offspring.append(offspring[0])
    return offspring


def mutation(offspring: dict, mutation_probability: float) -> dict:
    # checking if offspring should mutate by using uniform distribution
    rand = random.uniform(0,1)
    if rand <= mutation_probability:
        # generate two different random indexes to swap values between them
        rand_idx_to_mutate_1 = random.randint(0,9)
        rand_idx_to_mutate_2 = random.randint(0,9)
        while rand_idx_to_mutate_1 == rand_idx_to_mutate_2:
            rand_idx_to_mutate_2 = random.randint(0,9)
        value_safe_box = offspring[rand_idx_to_mutate_1]
        offspring[rand_idx_to_mutate_1] = offspring[rand_idx_to_mutate_2]
        offspring[rand_idx_to_mutate_2] = value_safe_box
    return offspring


def main():
    # reading data
    cities_file = np.loadtxt('Data\cities_4.txt').T

    # population size
    population_size = 250
    # parent to population population size ratio
    n = 0.8
    # probability of mutation
    mutation_probability = 0.2
    # number of iterations
    num_of_iter = 1000
    # algorithm used to select parents from population
    selection = "roulette_wheel"
    # selection = "kbest"

    best_score = genetic_algorithm(cities_file,
                                   population_size,
                                   num_of_iter,
                                   n ,
                                   mutation_probability,
                                   selection)
    print(best_score)

if __name__ == '__main__':
    main()
