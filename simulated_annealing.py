import numpy as np
import random
from scipy.spatial import distance
from typing import Tuple


def simulated_annealing(cities: np.array,
                        initial_temperature: float,
                        alpha: float,
                        beta: float,
                        scheduling: str) -> Tuple[float, float]:
    num_of_iter = 10000
    num_of_cities = cities.shape[0]
    temperature = initial_temperature
    element = dict()
    best_element = generate_one_path(num_of_cities)
    best_element = evaluate_cost(best_element, cities)

    minimum_temperature = 1  

    while num_of_iter != 0 or temperature < minimum_temperature:
        element = generate_one_path(num_of_cities)
        element = evaluate_cost(element, cities)
        if element['dist_traveled'] < best_element['dist_traveled']:
            best_element = element
        else:
            rand = random.uniform(0, 1)
            if rand < np.exp((best_element['dist_traveled'] - element['dist_traveled'])/initial_temperature):
                best_element = element

        # temperature scheduling
        if scheduling == 'exponential':
            temperature = alpha*temperature
        elif scheduling == 'inverse':
            temperature = temperature/(1+beta*temperature)

        num_of_iter -= 1

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
    for list_idx in range(1, len(element['path'])):
        actual_city = cities[element['path'][list_idx]]
        previous_city = cities[element['path'][list_idx - 1]]
        element['dist_traveled'] += distance.euclidean(actual_city, previous_city)
    return element


def main():
    cities = np.loadtxt(r"Data\cities_4.txt").T
    initial_temperature = 10**6
    alpha = 0.9999
    beta = 1 - alpha
    scheduling = 'exponential'
    best_score, best_path = simulated_annealing(cities, initial_temperature, alpha, beta, scheduling)
    print(best_score, best_path)


main()
