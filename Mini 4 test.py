import numpy as np
import matplotlib.pyplot as plt


# Placeholder functions for ELOPE (Evolutionary Layout Optimization Playground and Evaluator)
def generate_initial_population(size, layout_size):
    return [np.random.rand(*layout_size) for _ in range(size)]


def evaluate_fitness(population, constraints):
    return [np.sum(layout) for layout in population]


def select_parents(population, fitness_values):
    sorted_indices = np.argsort(fitness_values)
    return [population[i] for i in sorted_indices[-2:]]


def crossover(parents):
    crossover_point = np.random.randint(1, len(parents[0]))
    child1 = np.vstack((parents[0][:crossover_point], parents[1][crossover_point:]))
    child2 = np.vstack((parents[1][:crossover_point], parents[0][crossover_point:]))
    return [child1, child2]


def mutate(child, mutation_rate):
    mutation_mask = np.random.rand(*child.shape) < mutation_rate
    child[mutation_mask] = np.random.rand(*child.shape)[mutation_mask]
    return child


# Genetic Algorithm
def genetic_algorithm(num_machines, area, num_operations, cycle_time, max_generations):
    population_size = 10
    layout_size = (num_machines, num_operations)

    # Placeholder: Constraints
    constraints = {
        'area': area,
        'max_machines_per_row': 10,
        'max_machines_per_column': 10
    }

    generation = 0

    # Generate initial population
    population = generate_initial_population(population_size, layout_size)

    while generation < max_generations:
        # Evaluate fitness
        fitness_values = evaluate_fitness(population, constraints)

        # Select parents
        parents = select_parents(population, fitness_values)



        # Perform crossover to create offspring
        offspring = crossover(parents)

        # Perform mutation on offspring
        mutated_offspring = [mutate(child, mutation_rate=0.1) for child in offspring]

        # Replace the old population with the new generation
        population = mutated_offspring

        generation += 1

    best_layout = population[np.argmax(fitness_values)]
    return best_layout

if __name__ == "__main__":
    # Example inputs
    print("Enter No of Machines:")
    num_machines = int(input())
    print("Enter the area the industry in sq m")
    area = int(input())  # in square meters
    print("Enter the no of operations:")
    num_operations = int(input())
    cycle_time = [5, 7, 8, 10, 6]  # cycle time for each operation
    max_generations = 50
    print(num_machines," ",area," ",num_operations)
    best_layout = genetic_algorithm(num_machines, area, num_operations, cycle_time, max_generations)

    print("Best Plant Layout:")
    print(best_layout)

#Visualize

def visualize_layout(layout):
    plt.imshow(layout, cmap='viridis', interpolation='nearest')
    plt.title('Plant Layout')
    plt.xlabel('Machines')
    plt.ylabel('Operations')
    plt.colorbar(label='Machine Presence')
    plt.show()

if __name__ == "__main__":
    visualize_layout(best_layout)
