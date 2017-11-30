class Matrix:
    m = 0
    n = 0
    values = []

    def __init__(self, matrixs):
        self.values = []
        self.m = len(matrixs)
        assert(self.m > 0, '参数必须是一个二维列表')
        self.n = len(matrixs[0])
        for row in matrixs:
            assert(len(row) == self.n, '每一行列数必须相等')
            rows = []
            for col in row:
                rows.append(col)
                # print(col)
            self.values.append(rows)
        # self.values = matrixs

    def __str__(self):
        value_str_list = []
        for i in range(self.m):
            start = ' '
            end = ','
            if i == self.m - 1:
                end = ''
            if i == 0:
                start = ''
            value_str_list.append(start + str(self.values[i]) + end)
        value_str = '[' + '\n'.join(value_str_list) + ']'
        return value_str

    def __getitem__(self, index):
        return self.values[index]

    def size(self):
        return (self.m, self.n)

    def rows(self):
        # rows = []
        for row in self.values:
            mrow = Matrix([row])
            yield mrow
            # rows.append(mrow)
        # return rows

    def cols(self):
        rcols = []
        # cols = []
        for j in range(self.n):
            rcols.append([])
        for i in range(self.m):
            for j in range(self.n):
                rcols[j].append([self.values[i][j]])
        for col in rcols:
            mcol = Matrix(col)
            # cols.append(mcol)
            yield mcol
        # return cols

    def T(self):
        return Matrix(list(zip(*self.values)))

    def det(self):
        assert(self.m == self.n, '必须是一个方阵')
