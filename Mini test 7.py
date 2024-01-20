import numpy as np
import matplotlib.pyplot as plt

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

def visualize_layout(layout, build_area, machine_marker='o'):
    plt.figure(figsize=(8, 8))
    
    # Extracting machine positions from the layout
    machine_positions = np.where(layout > 0.5)

    # Plotting square build area
    plt.fill_between([0, build_area], 0, build_area, color='lightgray', label='Build Area')

    # Plotting machine positions with markers
    plt.scatter(machine_positions[1], machine_positions[0], marker=machine_marker, label='Machine', color='blue', s=100)

    plt.title('Optimized Plant Layout with Machine Representation')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    plt.show()

def optimize_plant_layout(num_machines, build_area, num_operations, max_generations):
    population_size = 10
    layout_size = (num_machines, num_operations)

    # Placeholder: Constraints
    constraints = {
        'max_machines_per_row': 100,
        'max_machines_per_column': 100
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
    visualize_layout(best_layout, build_area)

if __name__ == "__main__":
    # Example inputs
    num_machines = 10
    build_area = 100  # assuming a square-shaped factory (in square meters)
    num_operations = 5
    max_generations = 50

    optimize_plant_layout(num_machines, build_area, num_operations, max_generations)
