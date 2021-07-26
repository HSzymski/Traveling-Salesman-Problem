import numpy


def genetic_algorithm(cities_file: np.array,
                      p: int,
                      num_of_iter: int,
                      n: float,
                      mutation_probability: float) -> int:
    create_initial_population()

    while i in range(num_of_iter):
        evaluate_cost()
        create_parent_population()

        offspring_array_size = 0
        while offspring_array_size == n*p:
            create_offspring()


        create_parent_population()

    pass


def create_initial_population():
    pass


def evaluate_cost():
    pass


def mutaation():
    pass


def create_offspring():
    mutation()
    pass


def main():
    # reading data
    cities_file = np.loadtxt("Data\cities_4.txt").T

    # population size
    p = 250
    # parent to population population size ratio
    n = 0.8
    # probability of mutation
    mutation_probability = 0.2
    # number of iterations
    num_of_iter = 1000

    best_score = genetic_algorithm(cities_file, p, num_of_iter, n , mutation_probability)
    print(best_score)

if __name__ == '__main__':
    main()
