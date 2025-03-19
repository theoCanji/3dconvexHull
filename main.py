import math
import time
from RandomIncHull import RandomIncrementalHull3D
import helpers
import matplotlib.pyplot as plt

def time_algorithm(n_values, i, decrement_i = True):
    """
    Times the algorithm for different values of n, ensuring that the total time is > 1 second for accurate timing

    Args:
        n_values (list[int]): list of n values to test
        i (int): number of iterations to start with
    """
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
        if decrement_i and total_time > 2 and iterations >= 10:
            iterations = iterations//2
        print(f"n = {n:5d} | Average Time = {avg_time:.4f} sec over {iterations:2d} iterations | Total Time = {total_time:.4f} sec")
        total_time = 0
  
    # Plot the runtime, seems to be O(n)
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, results, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of Points (n)')
    plt.ylabel('Average Time (seconds) Over 100 Iterations')
    plt.title('Runtime of Randomized Incremental Convex Hull in 3D')
    plt.grid(True)
    plt.savefig('runtime.png')
    plt.show()

def visualize_hull(n: int):
    """
    Show the hull for n points for demo

    Args:
        n (int): number of points to generate and show
    """
    points = helpers.generate_random_points(n)
    hull = RandomIncrementalHull3D(points)
    hull.plot()
    print(helpers.is_convex(hull.get_hull())) ##verify correctness of the algorithm


def main():
    """
    main function to demonstrate runtime and the algo for a smaller n
    """
    n_values = [16000, 24000, 32000, 48000, 64000, 96000, 128000, 192000, 256000]
    n = 100
    
    # time_algorithm(n_values, 10)
    visualize_hull(n)
    
    
if __name__ == '__main__':
    main()
