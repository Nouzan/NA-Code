"""
多项式库
"""


class Polynomial():
    """
    多项式类
    """
    order = 0
    coefficients = [0]

    def __init__(self, coffs=[0]):
        if len(coffs) > 0:
            for i in range(1, len(coffs)):
                if coffs[i] != 0:
                    self.order = i
            self.coefficients = coffs[:self.order + 1]

    def __str__(self):
        coffStrList = []
        if self.coefficients[0] != 0:
            coffStrList = [str(self.coefficients[0])]
        for i in range(1, self.order + 1):
            if self.coefficients[i] != 0:
                # TODO：给负系数项加括号
                if self.coefficients[i] != 1:
                    coffStr = str(self.coefficients[i])
                else:
                    coffStr = ''
                if i > 1:
                    coffStrList.append(coffStr + 'x^' + str(i))
                else:
                    coffStrList.append(coffStr + 'x')
        return ' + '.join(coffStrList)

    def __add__(self, poly):
        if type(poly) == type(self):
            if self.order > poly.order:
                coffs1 = self.coefficients
                coffs2 = poly.coefficients
            else:
                coffs1 = poly.coefficients
                coffs2 = self.coefficients
            coffs = []
            for i in range(len(coffs2)):
                coffs.append(coffs1[i] + coffs2[i])
            for coff in coffs1[len(coffs2):]:
                coffs.append(coff)
            return Polynomial(coffs)

    def __rmul__(self, k):
        if isinstance(k, int):
            coffs = []
            for coff in self.coefficients:
                coffs.append(k*coff)
            return Polynomial(coffs)

    def __mul__(self, k):
        if isinstance(k, int):
            coffs = []
            for coff in self.coefficients:
                coffs.append(k*coff)
            return Polynomial(coffs)
        elif type(k) == type(self):
            # TODO: 多项式乘法
            return None

    def __neg__(self):
        return (-1) * self

    def __sub__(self, poly):
        if type(poly) == type(self):
            return self + (-poly)

    # TODO：重载除法，实现除法版本的数乘及多项式除法

    def qin9shao(self, x=0):
        """
        秦九韶算法
        """
        coffs = self.coefficients.copy()
        coffs.reverse()
        bList = [coffs[0]]
        for i in range(1, self.order + 1):
            bList.append(bList[i - 1] * x + coffs[i])
        bList.reverse()
        return (bList[0], Polynomial(bList[1:]))

    def dPoly(self, x=0, d=0):
        """
        利用秦九韶算法求导
        """
        if d == 0:
            return Polynomial(self.coefficients)
        else:
            p = self.dPoly(x, d-1)
            _, q = p.qin9shao(x)
            return d * q

    def D(self, x=0, d=1):
        if 0 <= d <= self.order:
            return self.dPoly(x, d)(x)
        else:
            return 0

    def __call__(self, x=0):
        b, q = self.qin9shao(x)
        return b
