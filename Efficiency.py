import numpy as np
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt

# Constants
NUM_MACHINES = 5
BUILD_AREA_SIZE = 20
MACHINE_AREA_SIZE = 2
TAKT_TIMES = np.array([1, 2, 3, 4, 5], dtype=np.float64)
LEAN_PARAMETERS = np.array([0.1, 0.2, 0.3, 0.4, 0.5])

# Create types for the individual and fitness
creator.create("FitnessMulti", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Initialize the toolbox
toolbox = base.Toolbox()

# Custom initialization method
def generate_individual():
    return [np.random.choice([-1, 0]) for _ in range(BUILD_AREA_SIZE**2)]

toolbox.register("individual", tools.initIterate, creator.Individual, generate_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Evaluation function
def evaluate_layout(individual):
    layout = np.array(individual).reshape((NUM_MACHINES, int(BUILD_AREA_SIZE/5), BUILD_AREA_SIZE))

    # Calculate efficiency (minimize)
    efficiency = np.sum(layout * TAKT_TIMES[:, np.newaxis, np.newaxis]) / np.sum(TAKT_TIMES)

    # Reshape the lean parameters to match the layout shape
    reshaped_lean_parameters = LEAN_PARAMETERS[:, np.newaxis, np.newaxis]

    # Calculate lean score (minimize)
    lean_score = np.sum(reshaped_lean_parameters * layout) / np.sum(reshaped_lean_parameters)

    return efficiency, lean_score

toolbox.register("evaluate", evaluate_layout)

# Genetic Algorithm parameters
cxpb = 0.7
mutpb = 0.2
num_generations = 50

# Register genetic operators
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selNSGA2)

# Create initial population
pop_size = 100
population = toolbox.population(n=pop_size)

# Evaluate the entire population
fitnesses = list(map(toolbox.evaluate, population))

for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit

# Genetic Algorithm
for gen in range(num_generations):
    offspring = algorithms.varAnd(population, toolbox, cxpb=cxpb, mutpb=mutpb)
    fits = toolbox.map(toolbox.evaluate, offspring)
    
    for ind, fit in zip(offspring, fits):
        ind.fitness.values = fit

    # Select the next generation
    population = toolbox.select(offspring + population, k=pop_size)

# Print the Pareto front (non-dominated solutions)
pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
for ind in pareto_front:
    print(ind.fitness.values)
efficiencies = [ind.fitness.values[0] for ind in pareto_front]
lean_scores = [ind.fitness.values[1] for ind in pareto_front]

# Create a scatter plot
plt.scatter(efficiencies, lean_scores)
plt.xlabel('Efficiency')
plt.ylabel('Lean Score')
plt.title('Pareto Front')
plt.show()

