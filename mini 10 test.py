import numpy as np
import matplotlib.pyplot as plt
import random
import time
def create_optimized_layout(num_machines, operation_times, total_build_area, machine_areas, walk_area):
    # Validate input lengths
    assert len(operation_times) == num_machines
    assert len(machine_areas) == num_machines

    # Sort machines by operation time (assuming shorter operation time machines should be closer to the entry)
    sorted_machines = sorted(range(num_machines), key=lambda k: operation_times[k], reverse=True)

    # Initialize the layout grid
    layout_grid = np.full((total_build_area, total_build_area), -1, dtype=int)

    # Place machines in the layout
    current_position = (0, 0)
    for machine_number in sorted_machines:
        machine_width, machine_height = machine_areas[machine_number]

        # Find a suitable position for the machine with walk area
        position_found = False
        while not position_found:
            i, j = current_position
            if j + machine_width + walk_area <= total_build_area and i + machine_height <= total_build_area:
                # Check if the area is available (no overlap)
                if np.all(layout_grid[i:i + machine_height, j + walk_area:j + machine_width + walk_area] == -1):
                    layout_grid[i:i + machine_height, j + walk_area:j + machine_width + walk_area] = machine_number
                    position_found = True

                    # Update current position for the next machine
                    current_position = (i, j + machine_width + 2 * walk_area)
                else:
                    # Move to the next row if the current row is full
                    current_position = (current_position[0] + 1, 0)
            else:
                # Move to the next row if there is not enough space in the current row
                current_position = (current_position[0] + 1, 0)

    return layout_grid

def visualize_layout(layout_grid):
    plt.imshow(layout_grid, cmap='viridis', origin='upper')

    # Add a colorbar with machine numbers
    cbar = plt.colorbar(ticks=range(layout_grid.max() + 1))
    cbar.set_label('Machine Number')

    plt.show()

import numpy as np
import random

def calculate_efficiency(layout_grid, operation_times):
    total_operation_time = 0

    for row in layout_grid:
        for machine_number in row:
            if machine_number != -1:
                total_operation_time += operation_times[machine_number]

    return total_operation_time

start_time = time.time()

# Example usage
num_machines = 30

# Generate random operation times for each machine
operation_times = [random.randint(5, 20) for _ in range(num_machines)]

total_build_area = 26

# Generate random machine areas (width, height) for each machine
machine_areas = [(random.randint(2, 4), random.randint(2, 4)) for _ in range(num_machines)]

walk_area = 1

layout = create_optimized_layout(num_machines, operation_times, total_build_area, machine_areas, walk_area)
visualize_layout(layout)

# Calculate efficiency
efficiency = calculate_efficiency(layout, operation_times)

print(f"Layout Efficiency: {efficiency} units of time")

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution Time: {execution_time} seconds")

