import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Function to generate an initial layout
def generate_initial_layout(num_machines, build_area_size, machine_area_size):
    layout = np.zeros((build_area_size, build_area_size))
    
    for _ in range(num_machines):
        machine_x, machine_y = np.random.randint(0, build_area_size - machine_area_size + 1, size=2)
        layout[machine_x: machine_x + machine_area_size, machine_y: machine_y + machine_area_size] = 1
    
    return layout

# Function to evaluate the fitness of a layout
def evaluate_layout(layout, num_machines, build_area_size, machine_area_size, takt_times, lean_parameters):
    num_unique_machines = len(np.unique(layout))
    coverage = np.sum(layout) / (num_machines * machine_area_size**2)
    diversity = num_unique_machines / num_machines
    
    # Calculate efficiency for each machine individually
    efficiency = np.sum([takt * np.sum(layout == (i + 1)) for i, takt in enumerate(takt_times)]) / np.sum(takt_times)
    
    # Flatten the layout to ensure consistent array sizes
    flat_layout = layout.flatten()
    
    # Distribute lean_parameters over flattened layout
    distributed_lean = np.tile(lean_parameters, len(flat_layout) // len(lean_parameters))
    
    # Calculate lean score using distributed lean_parameters
    lean_score = np.sum(distributed_lean * flat_layout) / np.sum(distributed_lean)

    return coverage, diversity, efficiency, lean_score


# Function to visualize a layout
def visualize_layout(layout, build_area_size, machine_area_size):
    plt.figure(figsize=(8, 8))
    
    # Plot build area
    plt.fill_between([0, build_area_size], 0, build_area_size, color='white', label='Build Area')

    # Extract machine positions
    machine_positions = np.argwhere(layout == 1)

    # Plot machines with different colors
    for machine_id, (machine_x, machine_y) in enumerate(machine_positions):
        color = plt.cm.get_cmap('tab10')(machine_id % 10)
        plt.fill_between([machine_y, machine_y + machine_area_size], machine_x, machine_x + machine_area_size, color=color, alpha=0.7, label=f'Machine {machine_id + 1}')

    plt.title('Optimized Plant Layout with Machine Representation')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid(True)
    plt.show()

# Genetic Algorithm setup
creator.create("FitnessMulti", base.Fitness, weights=(1.0, 1.0, 1.0, 1.0))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMulti)


toolbox = base.Toolbox()
toolbox.register("individual", generate_initial_layout, num_machines=5, build_area_size=20, machine_area_size=2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate_layout)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selNSGA2)

# Main optimization function
def optimize_plant_layout(num_machines, build_area_size, machine_area_size, takt_times, lean_parameters, generations=50):
    population_size = 50

    # Create an initial population
    population = toolbox.population(n=population_size)

    # Evaluate the entire population
    fitnesses = list(map(lambda ind: toolbox.evaluate(ind, num_machines, build_area_size, machine_area_size, takt_times, lean_parameters), population))

    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    # Begin the evolution
    algorithms.eaMuPlusLambda(population, toolbox, mu=50, lambda_=100, cxpb=0.7, mutpb=0.2, ngen=generations, stats=None, halloffame=None, verbose=True)

    # Get the Pareto front (non-dominated solutions)
    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]

    # Choose the best solution from the Pareto front
    best_solution = max(pareto_front, key=lambda x: sum(x.fitness.values))

    # Visualize the best solution
    visualize_layout(best_solution, build_area_size, machine_area_size)

if __name__ == "__main__":
    # Example inputs
    num_machines = 5
    build_area_size = 20
    machine_area_size = 2
    takt_times = np.array([2, 3, 1, 4, 2])
    lean_parameters = np.random.rand(num_machines)

    optimize_plant_layout(num_machines, build_area_size, machine_area_size, takt_times, lean_parameters)
