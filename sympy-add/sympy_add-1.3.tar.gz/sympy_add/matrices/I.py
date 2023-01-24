import numpy
import sympy
import re


class I(sympy.Matrix):
    """
    Класс единичной матрицы
    """
    def __new__(cls, i):
        return super().__new__(cls, numpy.eye(i, dtype='int8'))

    def P(self, i: int, j: int) -> sympy.Matrix:
    
        """
        Создает элементарную матрицу перемещающую строки

        Args:
            i (int): Индекс первой строки
            j (int): Индекс второй строки

        Returns:
            sympy.Matrix: Элементарная матрица
        """
        p_m = numpy.array(self)
        p_m[[i, j]] = p_m[[j, i]]
        return sympy.Matrix(p_m)

    def A(self, i: int, j: int, a: int = None) -> numpy.ndarray:
        """

        Создает элементарную матрицу прибавляющию к i-ой строке j-ую
            умножив на a, или вернет функцию в которую можно передать a
            позже        

        Args:
            i (int): Индекс строки к которой прибавлять
            j (int): Индекс строки которую прибвалять
            a (numpy.ndarray | function, optional): Число на которое надо домножить

        Returns: 
                function: Функция при вызове которой с передачей a вернется элементарная матрица
                numpy.ndarray: Элементарная матрица
        """
        def do(a):
            a = sympy.simplify(a)
            p_m = numpy.array(self)
            p_m[i, j] = a
            return sympy.Matrix(p_m)
        if a is None:
            return do
        return do(a)

    def M(self, i: int, a: int = None):
        """
        Создает элементарную матрицу умножающую i-ую строку на a

        Args:
            i (int): Индекс строки
            a (int, optional): Число на которое надо домножить

        Returns: 
                function: Функция при вызове которой с передачей a вернется элементарная матрица
                numpy.ndarray: Элементарная матрица
        """
        def do(a):
            a = sympy.simplify(a)
            p_m = numpy.array(self)
            p_m[[i]] *= a
            return sympy.Matrix(p_m)
        if a is None:
            return do
        return do(a)

    def __getattr__(self, key):
        if re.match(r'[APM]_', key):
            funcs = {'A': self.A, 'M': self.M, 'P': self.P}
            func, nums = key.split('_')
            nums = map(lambda x: int(x)-1, nums)
            return funcs[func](*nums)
        return super().__getattribute__(key)

    @staticmethod
    def cof_mat(T: numpy.ndarray) -> numpy.ndarray:
        """
        Составляет матрицу коэффицентов на которые домножаются строки

        Args:
            T (numpy.ndarray): Изначальная матрица

        Returns:
            numpy.ndarray: Матрица коэффицентов
        """
        T = T.copy()
        L = numpy.zeros(T.shape, dtype=object)

        L[:, -1] = T[:, -1]
        for column in range(T.shape[0]-2, -1, -1):
            T[column+1] /= T[column+1, column+1]
            for row in range(T.shape[0]):
                if row == column+1:
                    continue
                if column != T.shape[0]-1:
                    T[row] -= T[column+1]*T[row, column+1]
            L[:, column] = T[:, column]
        return L

    @staticmethod
    def decompose(mat: sympy.Matrix) -> list[numpy.array]:
        """
        Принимает квадратную матрицу, возвращает разложение
        на элементарные матрицы

        Args:
            mat (numpy.ndarray | sympy.Matrix | list): Квадратная матрица, 
            rref которой равен единичной

        Returns:
            list(numpy.ndarray): Список из элементарных numpy матриц
        """
        if isinstance(mat, sympy.Matrix) or isinstance(mat, list):
            mat = numpy.array(mat)

        matrices = []
        shape = mat.shape[0]
        mat = I.cof_mat(mat)
        i = I(shape)
        for col in range(shape):
            for row in range(shape):
                if row != col:
                    matrices.append(i.A(row, col, mat[row, col]))
            matrices.append(i.M(col, mat[col, col]))

        return matrices[::-1]


def main():
    n = I(3)

    A = sympy.Matrix([[11, 2, 3],
                      [-4, 5, -6],
                      [7, 8, 9]])

    k = I.decompose(A)
    for m in k:
        n *= m

    print(A == n, k)


if __name__ == "__main__":
    main()
