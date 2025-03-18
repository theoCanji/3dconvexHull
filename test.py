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
        print(f"n = {n:5d} | Average Time = {avg_time:.4f} sec over {iterations:2d} iterations | Total Time = {total_time:.4f} sec")
        total_time = 0
  
    # Plot the runtime, seems to be O(n)
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, results, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of Points (n)')
    plt.ylabel('Average Time (seconds)')
    plt.title('Runtime of RandomIncrementalHull3D')
    plt.grid(True)
    plt.show()

def visualize_hull(n: int):
    points = helpers.generate_random_points(n)
    hull = RandomIncrementalHull3D(points)
    hull.plot()
    print(helpers.is_convex(hull.get_hull())) ##verify correctness of the algorithm


def main():
    n_values = [500, 1000, 2000, 4000, 8000, 16000, 32000, 64000]
    n = 100
    time_algorithm(n_values, 75)
    visualize_hull(n)
    
    
if __name__ == '__main__':
    main()
    

    



