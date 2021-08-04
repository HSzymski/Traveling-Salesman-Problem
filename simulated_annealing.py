import numpy as np
import random
from scipy.spatial import distance
from typing import Tuple


def simulated_annealing(cities: np.array,
                        initial_temperature: float,
                        minimum_temperature: float,
                        alpha: float,
                        beta: float,
                        scheduling: str) -> Tuple[float, float]:
    num_of_cities = cities.shape[0]
    temperature = initial_temperature
    # generate random solution and set it as the best, calculate distance between cities
    best_element = generate_one_path(num_of_cities)
    best_element = evaluate_cost(best_element, cities)

    element = {}
    while temperature > minimum_temperature:
        # mutation of the best solution, calculate distance between cities
        element = swap_mutation(best_element)
        element = evaluate_cost(element, cities)
        # if new solution is better than actual best change elements, else check probability
        # of accepting worst solution with random number
        if element['dist_traveled'] < best_element['dist_traveled']:
            best_element = element
        else:
            rand = random.uniform(0, 1)
            p = np.exp((best_element['dist_traveled'] - element['dist_traveled'])/temperature)
            if rand < p:
                best_element = element

        # temperature scheduling
        if scheduling == 'exponential':
            temperature = alpha*temperature
        elif scheduling == 'inverse':
            temperature = temperature/(1+beta*temperature)

    best_score = element['dist_traveled']
    best_path = element['path']
    return best_score, best_path


def generate_one_path(num_of_cities: int) -> dict:
    # create list of indexes
    list_of_cities_idx = [idx for idx in range(num_of_cities)]
    # (shuffle method works in place and returns nothing)
    random.shuffle(list_of_cities_idx)
    # add idx of the first city
    list_of_cities_idx.append(list_of_cities_idx[0])
    return {'path': list_of_cities_idx, 'dist_traveled': 0}


def evaluate_cost(element: dict, cities: np.array) -> dict:
    # calculate euclidean dist between each cities and sum up them
    for list_idx in range(1, len(element['path'])):
        actual_city = cities[element['path'][list_idx]]
        previous_city = cities[element['path'][list_idx - 1]]
        element['dist_traveled'] += distance.euclidean(actual_city, previous_city)
    return element


def swap_mutation(best_element: dict) -> dict:
    # copy dictionary to avoid changing of original dictionary and change its distance to 0
    element = best_element.copy()
    element['dist_traveled'] = 0
    # cut off last city - the same as first (return of the salesman to source city)
    path = best_element['path'][:-1]
    # choose to different indexes and swap element of the list using it
    city_idx_1 = random.randint(0, len(path)-1)
    city_idx_2 = random.randint(0, len(path)-1)
    while city_idx_2 == city_idx_1:
        city_idx_2 = random.randint(0, len(path)-1)
    path[city_idx_1], path[city_idx_2] = path[city_idx_2], path[city_idx_1]
    # return of the salesman
    path.append(path[0])
    # rewrite changed element
    element['path'] = path
    return element


def main():

    cities = np.loadtxt(r"Data\cities_4.txt").T
    initial_temperature = 10*6
    minimum_temperature = 0.01
    alpha = 0.998
    beta = 1 - alpha
    # scheduling = 'exponential'
    scheduling = 'inverse'
    best_score, best_path = simulated_annealing(cities,
                                                initial_temperature,
                                                minimum_temperature,
                                                alpha,
                                                beta,
                                                scheduling)
    print(best_score, best_path)


main()
