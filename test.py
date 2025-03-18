import time
from RandomIncHull import RandomIncrementalHull3D
import helpers

def time_algorithm(n_values, i):
    total_time = 0
    iterations = i
    for n in n_values:
        for i in range(iterations):
            points = helpers.generate_random_points(n)
            start = time.time()
            RandomIncrementalHull3D(points)
            elapsed = time.time() - start
            total_time += elapsed
        avg_time = total_time / iterations
        if total_time > 2:
            iterations = iterations//2
        print(f"n = {n:5d} | Average Time = {avg_time:.4f} sec over {iterations} iterations | Total Time = {total_time:.4f} sec")
        total_time = 0
  
    return avg_time, iterations

n_values = [100, 200, 400, 800, 1600]
results = []

time_algorithm(n_values, 250)

