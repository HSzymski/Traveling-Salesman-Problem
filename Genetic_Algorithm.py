import numpy


def genetic_algorithm(cities_file: np.array) -> int:
    create_initial_population()
    evaluate_cost()
    pass


def create_initial_population():
    pass


def evaluate_cost():
    pass


def main():
    # reading data
    cities_file = np.loadtxt("Data\cities_4.txt").T

    # population size
    p = 250
    # offspring to parent population size ratio
    n = 0.8
    # probability of mutation
    mutation_probability = 0.2
    # number of iterations
    num_of_iter = 1000

    best_score = genetic_algorithm(cities_file)
    print(best_score)

if __name__ == '__main__':
    main()