# Generate some random convex polygon
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

class polygon(object):

    # generate random convex polygon by:
    # 1. generate a random set of points
    # 2. computing the convex hull of the points

    def __init__(self, points, size=100, num_point=30):
        
        self.size = size

        self.points = points

        self.hull = ConvexHull(self.points)

    def plot(self, plot=True):

        plt.plot(self.points[:,0], self.points[:,1], 'o')

        for simplex in self.hull.simplices:
            plt.plot(self.points[simplex, 0], self.points[simplex, 1], 'k-')

        if plot:
            plt.show()

if __name__ == "__main__":

    p = polygon()

    p.plot()