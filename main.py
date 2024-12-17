import numpy as np
import matplotlib.pyplot as plt

# Constants
alpha = 60  # Launch angle in degrees
way_length = 1200  # Target distance
object_length = 30  # Target size
g = 9.8  # Gravitational acceleration

variance_velocity = 2.0  # Standard deviation of velocity Этот параметр можно менять
variance_alpha = 0.2  # Standard deviation of angle Этот  параметр можно менять

quantity = 50000  # Number of shots
step = 100  # Step size for expectation and variance calculations
for_frequency = 600  # Range for frequency distribution
step_for_frequency = 50  # Step size for frequency distribution

# Calculate base velocity for hitting the target at exact `way_length`
velocity = np.sqrt((way_length * g) / np.sin(np.radians(2 * alpha)))

# Function to generate velocity using random numbers
def generate_velocity():
    random_values = np.random.random(12)
    return velocity + variance_velocity * (np.sum(random_values) - 6)

# Function to generate alpha using random numbers
def generate_alpha():
    random_values = np.random.random(12)
    return alpha + variance_alpha * (np.sum(random_values) - 6)

# Function to calculate bullet trajectory length
def calculate_bullet_way():
    return (generate_velocity()**2 * np.sin(np.radians(2 * generate_alpha()))) / g

# Simulate shots
array = np.zeros(quantity)
counter = 0  # Counter for hits
for i in range(quantity):
    array[i] = calculate_bullet_way()
    if way_length - object_length / 2 <= array[i] <= way_length + object_length / 2:
        counter += 1

# Calculate mathematical expectation
array_actual_values = np.zeros(quantity // step)
for i in range(len(array_actual_values)):
    array_actual_values[i] = np.mean(array[: (i + 1) * step])

# Plot mathematical expectation
plt.figure(figsize=(10, 6))
plt.plot(array_actual_values)
plt.title("График мат. ожидания")
plt.xlabel("Количество выстрелов")
plt.ylabel("Математическое ожидание")
plt.grid(True)
plt.show()

# Calculate variance
array_actual_variance = np.zeros(quantity // step)
for i in range(len(array_actual_variance)):
    array_actual_variance[i] = np.var(array[: (i + 1) * step], ddof=1)

# Plot variance
plt.figure(figsize=(10, 6))
plt.plot(array_actual_variance)
plt.title("График дисперсии")
plt.xlabel("Количество выстрелов")
plt.ylabel("Дисперсия")
plt.grid(True)
plt.show()

# Calculate frequency distribution
array_sorted = np.sort(array)
bins = np.arange(way_length - for_frequency, way_length + for_frequency + step_for_frequency, step_for_frequency)
frequencies = np.histogram(array_sorted, bins=bins)[0]

# Plot histogram
plt.figure(figsize=(10, 6))
plt.bar(bins[:-1], frequencies, width=step_for_frequency, align="edge")
plt.title("Частотный тест")
plt.xlabel("Длина траектории")
plt.ylabel("Частота")
plt.grid(True)
plt.show()

# Output results
print("Мат. ожидание = ", array_actual_values[-1])
print("Дисперсия = ", array_actual_variance[-1])
print("Вероятность попадания = {:.2f}".format(counter / quantity))
