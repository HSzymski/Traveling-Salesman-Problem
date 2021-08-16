# Traveling-Salesman-Problem
## Ant System

## Genetic Algorithm
In the field of computer science and operations research, is an derivative-free (do not need derivative to find optimal solution. Sometimes information about the derivative of the objective function is unavailable, unreliable or impractical to obtain), stochastic () algorithm which inspiration was the process of natural selection. 

Pseudocode:
1. Create initial population of P elements.
2. Evaluate the cost of each individual - the total distance to be traveled.
3. Using proportional selection choose n*P parents (0 < n <= 1).
4. Select randomly two parents and create offspring using Cycle Crossover Operator (CX).
5. Repeat the Step 4 until n*P offspring are generated.
6. Apply mutation operators (swap mutation) for changes in randomly selected offspring
7. Replace old parent population with the best P individuals (of minimum cost) from the combined parents and offspring populations.
8. Repeat the Step 2 until maximum number of generations were performed.

## Simulated Annealing

## Results
Tests was made for cities from cities_4.txt file, which consist of 10 cities placed in two dimensional space. Each algorithm was ran 30 times, working time and the best score (distance of the best route) were noticed.

The plot below was made for predefined parameters which gave the best results during the tests.
![results](https://user-images.githubusercontent.com/32731885/129105582-8953419c-e91b-4003-8af3-f37208ea314b.png)
According the plot above, 3 different times were defined (10, 20 and 30 seconds). That times were used as a stop criterion of the algorithms working. The conclusion of the efficiencies were drawn based on the results.

![results10](https://user-images.githubusercontent.com/32731885/129105325-dc40172c-0fa9-4933-a949-a771fba207b2.png)
![results20](https://user-images.githubusercontent.com/32731885/129105336-331bb4b0-bcf7-4fbb-b972-efa3dcfdbfe1.png)
![results30](https://user-images.githubusercontent.com/32731885/129105341-644fea54-2a4d-447f-8e59-ed5701a2ac82.png)


