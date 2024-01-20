import random

def generate_plant_layout(num_operations, num_machines, num_stations, cycle_time_at_each_station):
  """Generates a random plant layout blueprint for an industry.

  Args:
    num_operations: The number of operations in the industry.
    num_machines: The number of machines in the industry.
    num_stations: The number of stations in the industry.
    cycle_time_at_each_station: A list of the cycle times at each station.

  Returns:
    A list of lists, where each inner list represents a station and each element in
    the inner list represents a machine.
  """

  # Create a list of all the machines.
  machines = list(range(num_machines))

  # Randomly assign machines to stations.
  stations = []
  for i in range(num_stations):
    station = []
    for j in range(num_operations):
      machine = random.choice(machines)
      station.append(machine)
      machines.remove(machine)
    stations.append(station)

  # Calculate the cycle time of each station.
  station_cycle_times = []
  for station in stations:
    cycle_time = 0
    for machine in station:
      cycle_time += cycle_time_at_each_station[machine]
    station_cycle_times.append(cycle_time)

  # Return the plant layout blueprint.
  return stations, station_cycle_times

# Example usage:

num_operations = 10
num_machines = 5
num_stations = 3
cycle_time_at_each_station = [1, 2, 3, 4, 5]

stations, station_cycle_times = generate_plant_layout(num_operations, num_machines, num_stations, cycle_time_at_each_station)

print(stations)
print(station_cycle_times)