import numpy as np
import Polynomial as ply


class Interp():
    poly = ply.Polynomial()
    x = np.array([0], np.float)
    y = np.array([0], np.float)

    def __init__(self, xx, yy):
        self.x = np.array(xx, np.float)
        self.y = np.array(yy, np.float)

    def diffQuot(self, positions):
        if len(positions) == 1:
            result = self.y[positions[0]]
        elif len(positions) > 1:
            result = (self.diffQuot(positions[1:]) - self.diffQuot(positions[:-1]))/(self.x[positions[0]] - self.x[positions[-1]])
        else:
            result = 0
        return result
