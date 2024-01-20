import numpy as np
import matplotlib.pyplot as plt
import random

def create_optimized_layout(num_machines, machine_colors, operation_times, total_build_area, machine_areas, walk_area):
    # Validate input lengths
    assert len(machine_colors) == num_machines
    assert len(operation_times) == num_machines
    assert len(machine_areas) == num_machines

    # Sort machines by operation time (assuming shorter operation time machines should be closer to the entry)
    sorted_machines = sorted(range(num_machines), key=lambda k: operation_times[k], reverse=True)

    # Initialize the layout grid
    layout_grid = np.full((total_build_area, total_build_area), 'black', dtype=object)

    # Place machines in the layout
    current_position = (0, 0)
    for machine_idx in sorted_machines:
        machine_color = machine_colors[machine_idx]
        machine_width, machine_height = machine_areas[machine_idx]

        # Find a suitable position for the machine with walk area
        position_found = False
        while not position_found:
            i, j = current_position
            if j + machine_width + walk_area <= total_build_area and i + machine_height <= total_build_area:
                # Check if the area is available (no overlap)
                if np.all(layout_grid[i:i + machine_height, j + walk_area:j + machine_width + walk_area] == 'black'):
                    layout_grid[i:i + machine_height, j + walk_area:j + machine_width + walk_area] = machine_color
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

def visualize_layout(layout_grid, machine_colors):
    plt.imshow([[machine_colors.index(cell) if cell != 'black' else -1 for cell in row] for row in layout_grid], cmap='viridis', origin='upper')

    # Add a legend for machine colors
    legend_labels = [plt.Rectangle((0, 0), 1, 1, color=color) for color in machine_colors]
    plt.legend(legend_labels, machine_colors, loc='upper left', bbox_to_anchor=(1, 1))

    plt.show()

# Example usage
num_machines = 10

# Generate random colors for each machine type
machine_colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(num_machines)]

# Generate random operation times for each machine
operation_times = [random.randint(5, 20) for _ in range(num_machines)]

total_build_area = 40

# Generate random machine areas (width, height) for each machine
machine_areas = [(random.randint(2, 4), random.randint(2, 4)) for _ in range(num_machines)]

walk_area = 1

layout = create_optimized_layout(num_machines, machine_colors, operation_times, total_build_area, machine_areas, walk_area)
visualize_layout(layout, machine_colors)
