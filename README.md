# Traveling Salesman Problem
The Traveling Salesman Problem (TSP) is one of the well known benchmark for algorithms. In TSP there are a list of cities, in most cases with a fully grid of connections. The title salesman needs to visit all the cities and return to the starting one in a way that a total distance traveled is the shortest. Considering the symmetric TSP (TSP for which distance from i-th city to the j-th city is the same as from j-th to i-th), the number of possible solutions is (N-1)!/2.

## Ant System
Is a probabilistic technique for solving difficult computational problems. It's inspiration was the study of real ant traveling. While ants are traveling, they deposit on the ground a pheromone - substance which is used as a probability of choosing the same path by another ant. The more ants choose the same path the higher concentration of pheromone on that path is and the higher probability that others ants choose that path. From the other side there is also process called evaporation, decreasing concentration of pheromone over time. 

Psudocode of my implementation of Ant System:
1. Create initial population of k ants.
2. Move ant randomly to an unvisited city.
3. Repeat the Step 2 until ant visit all cities.
4. Calculate pheromone left by ant at each arc (path between two cities).
5. Repeat the Step 2 for each ant in population.
6. Update pheromone concentration on each arc.
7. Create another population of k ants.
8. Select next city to go from not visited yet by summing up probabilities of choosing pahts and uniform distribution.
9. Calculate probabilities of choosing each arc
10. Move ant to the unvisited city choosed by adding up successive probabilities and comparing them with a randomly generated number from uniform distribution.
11. Same as the Steps 3-6.
12. Repeat the Step 7 until maximum number of tours were achieved.


## Genetic Algorithm
In the field of computer science and operations research, genetic algorithm (GA) is an derivative-free (do not need derivative to find optimal solution, sometimes information about the derivative of the objective function is unavailable, unreliable or impractical to obtain), stochastic (being well described by a random probability distribution) algorithm, which inspiration was the process of natural selection - "Survival of the fittest"[1]. Finding optimal solution is achievable by biologically inspired operators such as mutation, crossover and selection[2].

A structure of a simple GA used to solve TSP problem, implemented in that repository:
1. Create initial population of P elements.
2. Evaluate the cost of each individual - the total distance to be traveled.
3. Using proportional selection choose n*P parents (0 < n <= 1).
4. Select randomly two parents and create offspring using Cycle Crossover Operator (CX).
5. Repeat the Step 4 until n*P offspring are generated.
6. Apply mutation operators (swap mutation) for changes in randomly selected offspring
7. Replace old parent population with the best P individuals (of minimum cost) from the combined parents and offspring populations.
8. Repeat the Step 2 until maximum number of generations were performed.

## Simulated Annealing
An optimization method which name comes from annealing in metallurgy, a technique involving heating and controlled cooling of a material to alter its physical properties. Each step of annealing has its representation in the code: temperature (range of search space exploration), getting new geometry (change of candidate solution) and cooling process (deceasing the range of exploration).

Pseudocode for Simulated Annealing:
1. Create initial path (candidate solution) and set temperature T.
2. Create new path.
3. If new path is better than previous, set it as a new candidate solution.
4. If new path is worse than previous check the probability of setting it as the new candidate solution.
5. Decrease the temperature T using cooling schedules.
6. Repeat the Step 2 until termination criterion was achieved.


## Results
Tests was made for cities from cities_4.txt file, which consist of 10 cities placed in two dimensional space. Each algorithm was ran 30 times, working time and the best score (distance of the best route) were noticed.

The plot below was made for predefined parameters which gave the best results during the tests.
![results](https://user-images.githubusercontent.com/32731885/129105582-8953419c-e91b-4003-8af3-f37208ea314b.png)
According the plot above, 3 different times were defined (10, 20 and 30 seconds). That times were used as a stop criterion of the algorithms working. The conclusion of the efficiencies were drawn based on the results.

![results10](https://user-images.githubusercontent.com/32731885/129105325-dc40172c-0fa9-4933-a949-a771fba207b2.png)
![results20](https://user-images.githubusercontent.com/32731885/129105336-331bb4b0-bcf7-4fbb-b972-efa3dcfdbfe1.png)
![results30](https://user-images.githubusercontent.com/32731885/129105341-644fea54-2a4d-447f-8e59-ed5701a2ac82.png)


[1] C. Darwin, On the origin of species by means of natural selection, or the preservation of favoured races in the struggle for life. London: John Murray, 1869. <br>
[2] Mitchell, Melanie, An Introduction to Genetic Algorithms. Cambridge, MA: MIT Press. ISBN 9780585030944, 1996.
