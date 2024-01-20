import numpy as np
import matplotlib.pyplot as plt
def get_machine_positions(layout):
    # Extracting machine positions from the layout
    machine_positions = np.where(layout > 0.5)
    return list(zip(machine_positions[0], machine_positions[1]))

def visualize_layout(layout, machine_marker='o'):
    plt.figure(figsize=(8, 6))

    # Extracting machine positions from the layout
    machine_positions = get_machine_positions(layout)

    # Plotting machine positions with markers
    plt.scatter([pos[1] for pos in machine_positions], [pos[0] for pos in machine_positions],
                marker=machine_marker, label='Machine', color='blue', s=100)

    plt.title('Plant Layout with Machine Representation')
    plt.xlabel('Machines')
    plt.ylabel('Operations')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Assuming the best_layout from the genetic_algorithm is a 2D matrix
    best_layout = np.array([[0.2, 0.8, 0.5, 0.1, 0.6],
                            [0.7, 0.3, 0.9, 0.4, 0.2],
                            [0.4, 0.6, 0.2, 0.8, 0.3],
                            [0.9, 0.1, 0.7, 0.2, 0.5],
                            [0.5, 0.4, 0.3, 0.6, 0.8],
                            [0.1, 0.7, 0.4, 0.9, 0.2],
                            [0.8, 0.5, 0.6, 0.3, 0.7],
                            [0.3, 0.9, 0.8, 0.7, 0.4],
                            [0.6, 0.2, 0.1, 0.5, 0.9],
                            [0.2, 0.6, 0.9, 0.4, 0.1]])

    machine_positions = get_machine_positions(best_layout)
    print("Machine Positions:", machine_positions)

    visualize_layout(best_layout)
