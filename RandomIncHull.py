import helpers
import DCEL
import random

class RandomIncrementalHull3D:
    def __init__(self, points):
        self.points = points
        self.hull = DCEL.DCEL()
        self.points = random.shuffle(points)
        self.hull.create_tetrahedron(points[0], points[1], points[2], points[3])
        self.hull.plot()

RandomIncrementalHull3D(helpers.generate_random_points(4))