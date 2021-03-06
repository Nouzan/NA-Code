import numpy as np
import matplotlib.pyplot as plt


class NewtonInterpolater():
    def __init__(self, xx=[], yy=[]):
        self.x = xx
        self.y = yy
        self.n = len(xx)
        self._diffQuotDict = {}
        if self.n > 0:
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
            if self.n > 0:
                self.a = min(self.x)
                self.b = max(self.x)
        return self

    def diffQuot(self, positions):
        result = self._diffQuotDict.get(str(positions), None)
        if result is None:
            if len(positions) == 1:
                result = self.y[positions[0]]
            elif len(positions) > 1:
                result = (
                    self.diffQuot(positions[1:]) -
                    self.diffQuot(positions[:-1])) / (self.x[positions[-1]] -
                                                      self.x[positions[0]])
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


class PiecewiseInterpolator():
    # count = list()
    def __init__(self, x, y):
        if len(x) > 0:
            # self.count.append(1)
            self.n = len(x)
            self.x = x.copy()  # 这里假定x列表已经从小到大排序
            self.y = y.copy()
            self.a = min(x)
            self.b = max(x)
            self.coffs = []

    def _interp(self):
        if len(self.coffs) == 0:
            for i in range(self.n - 1):
                k1 = self.y[i] / (self.x[i] - self.x[i + 1])
                k2 = self.y[i + 1] / (self.x[i + 1] - self.x[i])
                self.coffs.append((k1, k2))

    def __call__(self, x):
        self._interp()
        if isinstance(x, list):
            results = []
            for xx in x:
                # print(xx)
                results.append(self(xx))
            return results
        else:
            if self.a < x <= self.b:
                i = 0
                while x > self.x[i]:
                    i += 1
                k1, k2 = self.coffs[i - 1]
                result = k1 * (x - self.x[i]) + k2 * (x - self.x[i - 1])
            elif x == self.a:
                result = self.y[0]
            else:
                result = None
            return result

    def plot(self):
        x = list(np.linspace(self.a, self.b))
        plt.plot(x, self(x), self.x, self.y, 'rx')
        plt.show()


class PiecewiseHermiteInterpolator(PiecewiseInterpolator):
    def __init__(self, x, y, dy):
        super(PiecewiseHermiteInterpolator, self).__init__(x, y)
        self.dy = dy

    def _interp(self):
        if len(self.coffs) == 0:
            for i in range(self.n - 1):
                k1 = self.y[i] / (self.x[i] - self.x[i + 1]) ** 2
                k2 = self.y[i] * 2 / (self.x[i + 1] - self.x[i]) /\
                    (self.x[i] - self.x[i + 1]) ** 2
                k3 = self.y[i + 1] / (self.x[i + 1] - self.x[i]) ** 2
                k4 = self.y[i + 1] * 2 / (self.x[i] - self.x[i + 1]) /\
                    (self.x[i + 1] - self.x[i]) ** 2
                k5 = self.dy[i] / (self.x[i] - self.x[i + 1]) ** 2
                k6 = self.dy[i + 1] / (self.x[i + 1] - self.x[i]) ** 2
                self.coffs.append((k1, k2, k3, k4, k5, k6))

    def __call__(self, x):
        self._interp()
        if isinstance(x, list):
            results = []
            for xx in x:
                # print(xx)
                results.append(self(xx))
            return results
        else:
            if self.a < x <= self.b:
                i = 0
                while x > self.x[i]:
                    i += 1
                k1, k2, k3, k4, k5, k6 = self.coffs[i - 1]
                result = k1 * (x - self.x[i]) ** 2 + \
                    k2 * (x - self.x[i - 1]) * (x - self.x[i]) ** 2 +\
                    k3 * (x - self.x[i - 1]) ** 2 +\
                    k4 * (x - self.x[i]) * (x - self.x[i - 1]) ** 2 +\
                    k5 * (x - self.x[i]) ** 2 * (x - self.x[i - 1]) +\
                    k6 * (x - self.x[i - 1]) ** 2 * (x - self.x[i])
            elif x == self.a:
                result = self.y[0]
            else:
                result = None
            return result


class SplineInterpolator(PiecewiseInterpolator):
    def __init__(self, x, y, **kwargs):
        super(SplineInterpolator, self).__init__(x, y)
        if 'da' in kwargs and 'db' in kwargs:
            self.mode = 0
            self.da = kwargs['da']
            self.db = kwargs['db']
        elif 'dda' in kwargs and 'ddb' in kwargs:
            self.mode = 1
            self.dda = kwargs['dda']
            self.ddb = kwargs['ddb']
        elif 'is_periodic' in kwargs:
            if kwargs['is_periodic']:
                self.mode = 2
                # TODO:周期边界条件下的三次样条插值
        self._diffQuotDict = {}

    def _interp(self):
        self.m = [0] * self.n
        self.h = [0] * self.n
        self.miu = [0] * self.n
        self.lam = [0] * self.n
        self.d = [0] * self.n
        for i in range(self.n - 1):
            self.h[i] = self.x[i + 1] - self.x[i]
        for i in range(1, self.n - 1):
            self.miu[i] = self.h[i - 1] / (self.h[i - 1] + self.h[i])
            self.lam[i] = self.h[i] / (self.h[i - 1] + self.h[i])
            self.d[i] = 6 * self.diffQuot([i - 1, i, i + 1])

        if self.mode == 0:
            self.lam[0] = 1
            self.d[0] = 6 / self.h[0] * (self.diffQuot([0, 1]) - self.da)
            self.miu[self.n - 1] = 1
            self.d[self.n - 1] = 6 * self.h[self.n - 2] *\
                (self.db - self.diffQuot([self.n - 2, self.n - 1]))
            A = []
            D = []
            for i in range(0, self.n):
                D.append([self.d[i]])
                if i == 0:
                    A.append([2, self.lam[0]] + [0] * (self.n - 2 - i))
                elif i == self.n - 1:
                    A.append([0] * (i - 1) + [self.miu[i], 2])
                else:
                    A.append(
                        [0] * (i - 1) + [self.miu[i], 2, self.lam[i]] +
                        [0] * (self.n - 2 - i))
            A = np.array(A, np.float)
            # 解线性方程组：
            Ai = np.linalg.inv(A)
            D = np.array(D, np.float)
            M = np.dot(Ai, D)
            self.m = list(M.flatten())
            # print(self.m)
        elif self.mode == 1:
            self.lam[0] = self.miu[self.n - 1] = 0
            self.d[0] = self.dda * 2
            self.d[self.n - 1] = self.ddb * 2
            A = []
            D = []
            for i in range(0, self.n):
                D.append([self.d[i]])
                if i == 0:
                    A.append([2, self.lam[0]] + [0] * (self.n - 2 - i))
                elif i == self.n - 1:
                    A.append([0] * (i - 1) + [self.miu[i], 2])
                else:
                    A.append([0] * (i - 1) + [self.miu[i], 2, self.lam[i]] +
                             [0] * (self.n - 2 - i))
            A = np.array(A, np.float)
            Ai = np.linalg.inv(A)
            D = np.array(D, np.float)
            M = np.dot(Ai, D)
            self.m = list(M.flatten())

    def __call__(self, x):
        self._interp()
        if isinstance(x, list):
            results = []
            for xx in x:
                # print(xx)
                results.append(self(xx))
            return results
        else:
            if self.a < x <= self.b:
                i = 0
                while x > self.x[i]:
                    i += 1
                h = self.h[i - 1]
                result = self.m[i - 1] * (self.x[i] - x) ** 3 / (6 * h) +\
                    self.m[i] * (x - self.x[i - 1]) ** 3 / (6 * h) +\
                    (self.y[i - 1] - self.m[i - 1] * h * h / 6) / h *\
                    (self.x[i] - x) + (self.y[i] - self.m[i] * h * h / 6) /\
                    h * (x - self.x[i - 1])
            elif x == self.a:
                result = self.y[0]
            else:
                result = None
            return result

    def diffQuot(self, positions):
        result = self._diffQuotDict.get(str(positions), None)
        if result is None:
            if len(positions) == 1:
                result = self.y[positions[0]]
            elif len(positions) > 1:
                result = (
                    self.diffQuot(positions[1:]) -
                    self.diffQuot(positions[:-1])) /\
                    (self.x[positions[-1]] - self.x[positions[0]])
            else:
                result = 0
            self._diffQuotDict[str(positions)] = result
        return result
