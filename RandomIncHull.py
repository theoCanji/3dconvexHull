import helpers
import DCEL
import random

class RandomIncrementalHull3D:
    def __init__(self, points):
        self.points = points
        self.dcel = DCEL.DCEL()
        self.points = random.shuffle(points)
        