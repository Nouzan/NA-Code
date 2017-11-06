import Interpolator as ite
# import numpy as np


# x = np.array(list(range(-5, 6)), np.float)
# y = 1 / (1 + x ** 2)
# f = ite.SplineInterpolator(list(x), list(y), da=10/(26**2), db=-10/(26**2))
# f = ite.SplineInterpolator([0.25, 0.30, 0.39, 0.45, 0.53],
# [0.5, 0.5477, 0.6245, 0.6708, 0.7280], dda=0, ddb=0)
f = ite.SplineInterpolator([0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
                           [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                           da=0, db=1 / 20)
f.plot()

g = ite.NewtonInterpolater([0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
                           [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
g.plot()
