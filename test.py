import time
from RandomIncHull import RandomIncrementalHull3D
import helpers
import matplotlib.pyplot as plt

def time_algorithm(n_values, i):
    total_time = 0
    iterations = i
    results = []
    for n in n_values:
        for i in range(iterations):
            points = helpers.generate_random_points(n)
            start = time.time()
            RandomIncrementalHull3D(points)
            elapsed = time.time() - start
            total_time += elapsed
        avg_time = total_time / iterations
        results.append(avg_time)
        if total_time > 2:
            iterations = iterations//2
        print(f"n = {n:5d} | Average Time = {avg_time:.4f} sec over {iterations} iterations | Total Time = {total_time:.4f} sec")
        total_time = 0
  
    return results

n_values = [500, 1000, 2000, 4000, 8000, 16000, 32000, 64000]
results = time_algorithm(n_values, 75)

# Plot the runtime, seems to be O(n)
plt.figure(figsize=(10, 6))
plt.plot(n_values, results, marker='o', linestyle='-', color='b')
plt.xlabel('Number of Points (n)')
plt.ylabel('Average Time (seconds)')
plt.title('Runtime of RandomIncrementalHull3D')
plt.grid(True)
plt.show()



