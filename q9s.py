"""
秦九韶算法
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
        coffStrList = [str(self.coefficients[0])]
        for i in range(1, self.order + 1):
            if self.coefficients[i] != 0:
                # TODO：给负系数项加括号
                if i > 1:
                    coffStrList.append(str(self.coefficients[i]) + 'x^' + str(i))
                else:
                    coffStrList.append(str(self.coefficients[i]) + 'x')
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

    def __sub__(self, poly):
        if type(poly) == type(self):
            return self + (-poly)

    def __neg__(self):
        coffs = []
        for coff in self.coefficients:
            coffs.append(-coff)
        return Polynomial(coffs)

    # TODO：重载乘法，实现数乘（左右均可）及多项式乘法
    # TODO：重载除法，实现除法版本的数乘及多项式除法

    # TODO：实现秦九韶算法
