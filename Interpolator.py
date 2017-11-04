import numpy as np
import matplotlib.pyplot as plt


class NewtonInterpolater():
    n = 0
    x = []
    y = []
    a = None
    b = None
    _diffQuotDict = {}

    def __init__(self, xx=[], yy=[]):
        self.x = xx
        self.y = yy
        self.n = len(xx)
        if self.n > 0 :
            self.a = min(xx)
            self.b = max(xx)
        # self.diffQuot(list(range(self.n)))

    def __iadd__(self, point):
        if isinstance(point, list):
            for p in point:
                self += p
        else:
            x, y = point
            self.x.append(x)
            self.y.append(y)
            self.n += 1
            self.diffQuot(list(range(self.n)))
            if self.n > 0 :
                self.a = min(self.x)
                self.b = max(self.x)
        return self

    def diffQuot(self, positions):
        result = self._diffQuotDict.get(str(positions), None)
        if result is None:
            if len(positions) == 1:
                result = self.y[positions[0]]
            elif len(positions) > 1:
                result = (self.diffQuot(positions[1:]) - self.diffQuot(positions[:-1]))/(self.x[positions[-1]] - self.x[positions[0]])
            else:
                result = 0
            self._diffQuotDict[str(positions)] = result
        return result

    def printDiffQuotTable(self):
        # self.diffQuot(list(range(self.n)))
        for j in range(self.n):
            for i in range(j + 1):
                positions = list(range(i, j + 1))
                print(self.diffQuot(positions), end=' ')
            print('')
        # TODO: 嗯..均差表的输出有问题。

    def __call__(self, x):
        bases = [1]
        for i in range(self.n - 1):
            mul = bases[i] * (x - self.x[i])
            bases.append(mul)
            # print(bases)
        result = 0
        for i in range(self.n):
            positions = list(range(i + 1))
            result += self.diffQuot(positions) * bases[i]
        return result

    def plot(self):
        x = np.linspace(self.a, self.b)
        plt.plot(x, self(x), self.x, self.y, 'rx')
        plt.show()

    class PiecewistLinearInterpolator():
        n = 1
        x = [0]
        y = [0]
        a = 0
        b = 0

        def __init__(self, x, y, mode=0):
            if len(x) > 0:
                self.n = len(x)
                self.x = x
                self.y = y
                self.a = x[0]
                self.b = x[-1]
