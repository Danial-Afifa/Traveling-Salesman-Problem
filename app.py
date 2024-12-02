from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Number of clients:
num_customers = 10

# Number of individuals in the first generation:
population_size = 50

# Initialize the first generation with random individuals:
population = [random.sample(range(num_customers), num_customers) for _ in range(population_size)]

# Fitness Function:
def fitness(individual, distance_matrix):
    total_distance = sum(distance_matrix[individual[i-1]][individual[i]] for i in range(len(individual)))
    return -total_distance

# Selection of individuals for mating:
def selection(population, distance_matrix):
    population.sort(key=lambda x: fitness(x, distance_matrix), reverse=True)
    return population[:population_size // 2]  # Select the fittest half of the individuals

# Mating:
def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child1 = parent1[:crossover_point] + [x for x in parent2 if x not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [x for x in parent1 if x not in parent2[:crossover_point]]
    return child1, child2

# Genetic mutation:
def mutate(individual):
    idx1, idx2 = random.sample(range(len(individual)), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_simulation():
    num_generations = 100
    distance_matrix = [[random.randint(1, 100) for _ in range(num_customers)] for _ in range(num_customers)]
    
    global population

    for generation in range(num_generations):
        selected_individuals = selection(population, distance_matrix)
        new_population = []

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_individuals, 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.append(child1)
            new_population.append(child2)

        population = new_population

    best_solution = max(population, key=lambda x: fitness(x, distance_matrix))
    return jsonify({'solution': best_solution, 'fitness': -fitness(best_solution, distance_matrix)})

if __name__ == '__main__':
    app.run(debug=True)
