import numpy as np
import pandas as pd
import random
from scipy.spatial import distance

def ant_system(cities: np.array,
               k: int,
               num_of_tours: int,
               alpha: float,
               beta: float,
               p: float) -> float:

    num_of_cities = cities.shape[0]

    # calculate start level of the pheromone
    array_dist_between_cities = calc_distance_array(cities)
    max_dist = np.nanmax(array_dist_between_cities,axis=1)
    tau_0 = 1/max_dist

    # create dictionary of ants which will move through the cities
    dict_of_ants = create_ants(k,num_of_cities)

    # initialization of decision table
    array_base_pheromone = np.zeros((num_of_cities,num_of_cities))
    array_pheromone = np.copy(array_base_pheromone)
    for i in range(num_of_cities):
        for j in range(num_of_cities):
            if(i==j):
                array_base_pheromone[i][j] = np.nan
            else:
                array_base_pheromone[i][j] = tau_0[j]

    # in the first tour choose paths randomly
    for ant in dict_of_ants:
        for i in range(num_of_cities-1):
            # draw city number
            city_idx = random.choice(ant['cities_left'])

            # save information about the traveled route
            ant['cities_left'].remove(city_idx)
            ant['dist_traveled'] += distance.euclidean(cities[ant['path'][-1]], cities[city_idx])
            ant['path'].append(city_idx)

        # after visiting each city return to the starting place
        ant['dist_traveled'] += distance.euclidean(cities[ant['path'][-1]], cities[ant['start_point']])
        ant['path'].append(ant['start_point'])

        # sum up pheromone on each arc from this tour
        for first_city_idx, second_city_idx in \
                zip(ant['path'][:-1],ant['path'][1:]):
            array_pheromone[first_city_idx][second_city_idx] += 1 / ant['dist_traveled']

    # calculate level of pheromone between cities
    array_whole_pheromone = p*array_base_pheromone+array_pheromone

    # main loop of the algorithm
    for tour in range(num_of_tours):
        #dict_of_ants = create_ants(k, num_of_cities)
        dict_of_ants = restart_ants(dict_of_ants, num_of_cities)

        for ant in dict_of_ants:
            for i in range(num_of_cities-1):
                actual_city_idx = ant['path'][-1]
                semi_decision_table = np.zeros(shape=(num_of_cities,1))
                decision_table = np.zeros_like(semi_decision_table)

                for city_idx in range(num_of_cities):
                    # avoid same and visited cities
                    if city_idx == actual_city_idx or city_idx not in ant['cities_left']:
                        semi_decision_table[city_idx] = np.nan
                    else:
                        semi_decision_table[city_idx] = (array_whole_pheromone[actual_city_idx][city_idx]**\
                                                    alpha) * ((1/array_dist_between_cities[actual_city_idx][city_idx])**beta)
                for j in range(num_of_cities):
                    decision_table[j] = semi_decision_table[j]/\
                                        np.nansum(semi_decision_table)
                                        #np.nansum(decision_table[np.arange(len(decision_table))!=i])

                probabilities_table = np.zeros_like(decision_table)
                for k in range(num_of_cities):
                    if not np.isnan(probabilities_table[k]):
                        probabilities_table[k] = decision_table[k]/np.nansum(decision_table)

                city_to_go_idx = where_to_go(probabilities_table)

                # save information about the traveled route
                ant['cities_left'].remove(city_to_go_idx)
                ant['dist_traveled'] += distance.euclidean(cities[ant['path'][-1]], cities[city_to_go_idx])
                ant['path'].append(city_to_go_idx)

            # after visiting each city return to the starting place
            ant['dist_traveled'] += distance.euclidean(cities[ant['path'][-1]], cities[ant['start_point']])
            ant['path'].append(ant['start_point'])

            # sum up pheromone on each arc from this tour
            for first_city_idx, second_city_idx in \
                    zip(ant['path'][:-1], ant['path'][1:]):
                array_pheromone[first_city_idx][second_city_idx] += 1 / ant['dist_traveled']

        array_whole_pheromone = p*array_whole_pheromone+array_pheromone

    dict_of_ants = sorted(dict_of_ants, key=lambda ant: ant['dist_traveled'])
    best_dist = dict_of_ants[0]['dist_traveled']
    return best_dist

def create_ants(num_of_ants: int, num_of_cities: int) -> list:
    dict_of_ants = []
    for i in range(num_of_ants):
        rand_start_point = np.random.randint(0,num_of_cities-1)
        start_dist = 0
        ant = {"start_point":rand_start_point,"dist_traveled":start_dist,
               "cities_left":list(range(num_of_cities)), "path":[rand_start_point]}
        ant['cities_left'].remove(ant['start_point'])
        dict_of_ants.append(ant)
    return dict_of_ants


def restart_ants(dict_of_ants: list, num_of_cities: int) -> list:
    for ant in dict_of_ants:
        ant['dist_traveled'] = 0
        ant["cities_left"] = list(range(num_of_cities))
        ant['cities_left'].remove(ant['start_point'])
        ant['path'] = [ant['start_point']]
    return dict_of_ants


def where_to_go(probabilities_table: np.array) -> int:
    rand_num = np.random.uniform(0,1)
    sum_of_probabilities = 0
    index_of_city = -1
    for idx, val in enumerate(probabilities_table.reshape((-1,))):
        if not np.isnan(val):
            sum_of_probabilities += val
        if sum_of_probabilities >= rand_num:
            index_of_city = idx
            break
    if index_of_city == -1:
        for i in range(probabilities_table.shape[0]):
            if np.isnan(probabilities_table[-1-i]):
                continue
            else:
                index_of_city = i
    return index_of_city


def calc_distance_array(cities: np.array) -> np.array:
    num_of_cities = cities.shape[0]
    array_dist_between_cities = np.zeros((num_of_cities, num_of_cities))
    for i in range(num_of_cities):
        for j in range(num_of_cities):
            if(i==j):
                array_dist_between_cities[i][j] = np.nan
            else:
                city_dist = distance.euclidean(cities[i], cities[j])
                array_dist_between_cities[i][j] = city_dist
                array_dist_between_cities[j][i] = city_dist
    return array_dist_between_cities


def main():
    # reading data
    cities_file = np.loadtxt("Data\cities_4.txt").T

    # num of: ants/ cities
    k = cities_file.shape[0]
    # control parameters
    alpha = 1
    beta = 5
    # pheromone evaporation coefficient
    p = 0.5
    # number of iterations
    num_of_iter = 200

    best_score = ant_system(cities_file, k, num_of_iter, alpha, beta, p)
    print(best_score)

if __name__ == '__main__':
    main()
