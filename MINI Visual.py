import numpy as np
import matplotlib.pyplot as plt

def generate_random_layout(num_machines, layout_size):
    layout = np.zeros(layout_size, dtype=int)

    for _ in range(num_machines):
        x, y = np.random.randint(0, layout_size[0]), np.random.randint(0, layout_size[1])
        layout[x, y] = 1  # Assuming 1 represents a machine

    return layout

def visualize_layout(layout):
    plt.imshow(layout, cmap='viridis', interpolation='nearest')
    plt.title('Plant Layout')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.colorbar(label='Machine Presence')
    plt.show()

if __name__ == "__main__":
    num_machines = 10  # Adjust the number of machines
    layout_size = (10, 10)  # Adjust the layout size

    plant_layout = generate_random_layout(num_machines, layout_size)
    visualize_layout(plant_layout)
