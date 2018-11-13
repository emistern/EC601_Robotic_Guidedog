# Find the Chebyshev center of a convex polygon
import numpy as np
import matplotlib.pyplot as plt
from polygon import polygon
from numpy.linalg import norm
from scipy.optimize import linprog

class ChebyshevCenter(object):

    # Solve chebyshev center using linear programming

    def __init__(self, hull):

        self.poly = hull
        #self.poly = polygon(num_point=50)

    def showPolygon(self):

        self.poly.plot()

    def _transform(self):
        # Transform the problem into standard form
        #print(self.poly.points)
        A = []
        B = []
        c = [0, 0, -1]

        # choose one point that is not on the edge
        for i in range(len(self.poly.points)):
            if i not in self.poly.hull.simplices:
                inner_point_idx = i
                break
        inner_point = self.poly.points[inner_point_idx]
        #print ("inner Point: " + str(inner_point))

        for simplex in self.poly.hull.simplices:
            #print(simplex)
            #print(self.poly.points[simplex, 0], self.poly.points[simplex, 1])
            _x = self.poly.points[simplex, 0]
            _y = self.poly.points[simplex, 1]

            # The vector of shift
            x = _x[0] - _x[1]
            y = _y[0] - _y[1]

            # The two ends of an edge
            p1 = np.array([_x[0], _y[0]])
            p2 = np.array([_x[1], _y[1]])

            # determin the parameter for the line define by the edge
            k = y / x
            ofs = p1[1] - k * p1[0]

            # determin which side does the inner point reside
            sign = inner_point[1] < (inner_point[0] * k + ofs) # true indicates inner point under the line define be edge

            p3 = (0, 0)
            #b = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
            ofs_x = abs(- ofs / k)
            b = abs(ofs) * (ofs_x / np.sqrt(ofs_x ** 2 + ofs ** 2))
            a = np.array([-y, x]) / np.sqrt(x ** 2 + y ** 2)

            # adjust a and b according to sign
            if (a[0] > 0 and a[1] > 0):
                if (sign):
                    pass
                else:
                    a[0] = -a[0]
                    a[1] = -a[1]
                    #b = -b
            elif (a[0] < 0 and a[1] < 0):
                if (sign):
                    a[0] = -a[0]
                    a[1] = -a[1]
                else:
                    #b = -b
                    pass
            elif (a[0] > 0 and a[1] < 0):
                if (sign):
                    a[0] = -a[0]
                    a[1] = -a[1]
                    #b = -b
                else:
                    pass
            else:
                if (sign):
                    pass
                else:
                    a[0] = -a[0]
                    a[1] = -a[1]
                    #b = -b
            a = np.concatenate((a, [1]))
            A.append(a)
            B.append(b)
        A = np.array(A)
        B = np.array(B)
        c = np.array(c)
        print(A, B)
        return A, B, c

    def solve(self, show=False):

        A, b, c = self._transform()

        x0_bounds = (None, None)
        x1_bounds = (None, None)
        x2_bounds = (0, None)

        res = linprog([0, 0, -1], A_ub=A, b_ub=b, bounds=(x0_bounds, x1_bounds, x2_bounds), options={"disp": True})

        #print(res)
        if show:
            self.plot(res)

        return np.array([res['x'][0], res['x'][1]])

    def plot(self, res):

        self.poly.plot(plot=False)
        #print(res)
        center = (res['x'][0], res['x'][1])
        r = res['x'][2]
        
        circle = plt.Circle(center, r, color='b', fill=False)
        plt.plot([center[0]], [center[1]], 'g.', marker='o', markersize=10)
        ax = plt.gca()
        ax.add_artist(circle)
        
        plt.show()

if __name__ == "__main__":

    c = ChebyshevCenter()

    c._transform()

    #c.showPolygon()

    c.solve()

    