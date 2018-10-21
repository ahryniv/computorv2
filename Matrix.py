from    InputSyntaxException       import InputSyntaxException
import  Number
import  Complex
import  reverse_polish_notation

from decimal import Decimal

class Matrix:

    error_msg_syntax = 'Matrix syntax error in "{0}"'
    errot_msg_size = 'Matrix size error in "{0}"'

    def __init__(self, variables, functions):
        self.variables = variables
        self.functions = functions
        self.data = []
        self.string = ""
        self.columns = 0
        self.rows = 0

    def parse_string(self):
        opened = 0
        tmp = []
        value = ""
        for i, char in enumerate(self.string):
            if char == '[':
                opened += 1
            elif char == ']':
                if i + 1 != len(self.string) and self.string[i + 1] not in "];":
                    raise InputSyntaxException(self.error_msg_syntax.format(self.string))
                opened -= 1
                if opened < 0:
                    raise InputSyntaxException(self.error_msg_syntax.format(self.string))
                elif opened == 0:
                    if value:
                        self.add_value(value, tmp)
                    break
                if value:
                    value = self.add_value(value, tmp)
            elif char == ',':
                if not value:
                    raise InputSyntaxException(self.error_msg_syntax.format(self.string))
                value = self.add_value(value, tmp)
            elif char == ';':
                self.add_row(tmp)
                tmp = []
            else:
                value += char
        if tmp:
            self.add_row(tmp)
                
    def add_value(self, value, tmp):
        rpn = reverse_polish_notation.ReversePolishNotation(value, self.variables, self.functions)
        rpn.calculate()
        tmp.append(rpn.result)
        value = ""
        return value

    def add_row(self, row):
        if self.columns == 0:
            self.columns = len(row)
        elif self.columns != len(row):
            raise InputSyntaxException(self.errot_msg_size.format(self.string))
        self.data.append(row)
        self.rows = len(self.data)

    def add_symbol(self, char):
        self.string += char

    def get_columns_amount(self):
        return len(self.data[0])

    def get_rows_amount(self):
        return len(self.data)

    def get_reverse(self):
        determinant = self.get_determinant()
        if determinant == 0:
            raise InputSyntaxException("Determinant equals zero, matrix doesn't have reverse matrix")
        reverse_matrix = Matrix({}, {})
        for i in range(self.rows):
            tmp = []
            for j in range(self.columns):
                minor_matrix = self.get_minor(j, i)
                minor_det = minor_matrix.get_determinant() / determinant
                if (i + j) % 2 == 1:
                    minor_det *= Number.Number(-1)
                tmp.append(minor_det)
            reverse_matrix.add_row(tmp)
        return reverse_matrix

    def get_determinant(self):
        if self.rows != self.columns:
            raise InputSyntaxException("Determinant can be calculated only from square matrix")
        if self.rows == 0:
            raise InputSyntaxException("Determinant can't be calculated from empty matrix")
        if self.rows == 1:
            return self.data[0][0]
        elif self.rows == 2:
            return (self.data[0][0] * self.data[1][1]) - (self.data[0][1] * self.data[1][0])
        elif self.rows == 3:
            return (self.data[0][0] * self.data[1][1] * self.data[2][2]) + \
                    (self.data[0][1] * self.data[1][2] * self.data[2][0]) + \
                    (self.data[0][2] * self.data[1][0] * self.data[2][1]) - \
                    (self.data[0][2] * self.data[1][1] * self.data[2][0]) - \
                    (self.data[0][0] * self.data[1][2] * self.data[2][1]) - \
                    (self.data[0][1] * self.data[1][0] * self.data[2][2])
        else:
            determinant = Number.Number(0)
            for i in range(self.columns):
                result = []
                m_tmp = Matrix({}, {})
                for lst in self.data[1:]:
                    start = lst[:i]
                    end = lst[i + 1:] if i != self.columns - 1 else []
                    tmp = start + end
                    result.append('[{0}]'.format(','.join(map(str,tmp))))
                m_tmp.string = "[" + ";".join(result) + "]"
                m_tmp.parse_string()
                tmp_calc = self.data[0][i] * m_tmp.get_determinant()
                if i % 2 == 1:
                    tmp_calc = tmp_calc * Number.Number(-1)
                determinant += tmp_calc
            return determinant

    def get_minor(self, i, j):
        if self.rows != self.columns:
            raise InputSyntaxException("Minor can be calculated only from square matrix")
        minor = Matrix(self.variables, self.functions)
        for m in range( len(self.data) ):
            if m == i:
                continue
            tmp = []
            for n in range( len(self.data[m]) ):
                if n == j:
                    continue
                tmp.append(self.data[m][n])
            minor.add_row(tmp)
        return minor

    def __add__(self, x):
        if isinstance(x, Matrix):
            if x.get_rows_amount() != self.get_rows_amount() \
                    or x.get_columns_amount() != self.get_columns_amount():
                raise InputSyntaxException("Error while adding matrixes with different size")
            new_m = Matrix(self.variables, self.functions)
            for i, row in enumerate(self.data):
                tmp = []
                for j, item in enumerate(row):
                    tmp.append(self.data[i][j] + x.data[i][j])
                new_m.add_row(tmp)
            return new_m
        elif isinstance(x, Number.Number) and x.val == 0:
            return self
        else:
            raise InputSyntaxException('Error: You can\'t add Matrix with {0}'.format(type(x).__name__))
    
    def __sub__(self, x):
        if isinstance(x, Matrix):
            if x.get_rows_amount() != self.get_rows_amount() \
                    or x.get_columns_amount() != self.get_columns_amount():
                raise InputSyntaxException("Error while subtracting matrixes with different size")
            if x == self:
                return Number.Number(0)
            new_m = Matrix(self.variables, self.functions)
            for i, row in enumerate(self.data):
                tmp = []
                for j, item in enumerate(row):
                    tmp.append(self.data[i][j] + (x.data[i][j] * Number.Number(-1)))
                new_m.add_row(tmp)
            return new_m
        elif isinstance(x, Number.Number) and x.val == 0:
            return self
        else:
            raise InputSyntaxException('Error: You can\'t subtract Matrix with {0}'.format(type(x).__name__))

    def __mul__(self, x):
        if isinstance(x, Number.Number) or isinstance(x, Complex.Complex):
            new_m = Matrix(self.variables, self.functions)
            for i, row in enumerate(self.data):
                tmp = []
                for j, item in enumerate(row):
                    tmp.append(self.data[i][j] * x)
                new_m.add_row(tmp)
            return new_m
        elif isinstance(x, Matrix):
            if self.columns != x.rows:
                raise InputSyntaxException("Error while multiplying matrixes")
            new_m = Matrix(self.variables, self.functions)
            for i in range(self.rows):
                tmp = []
                for j in range(x.columns):
                    c = Number.Number(0)
                    for k in range(self.columns):
                        c += self.data[i][k] * x.data[k][j]
                    tmp.append(c)
                new_m.add_row(tmp)
            return new_m
        else:
            raise InputSyntaxException('Error: You can\'t multiply Matrix with {0}'.format(type(x).__name__))

    def __truediv__(self, x):
        if isinstance(x, Number.Number) or isinstance(x, Complex.Complex):
            new_m = Matrix(self.variables, self.functions)
            for i, row in enumerate(self.data):
                tmp = []
                for j, item in enumerate(row):
                    tmp.append(self.data[i][j] / x)
                new_m.add_row(tmp)
            return new_m
        elif isinstance(x, Matrix):
            reverse_matrix = x.get_reverse()
            return self * reverse_matrix
        else:
            raise InputSyntaxException('Error: You can\'t divide Matrix with {0}'.format(type(x).__name__))


    def __mod__(self, x):
        if isinstance(x, Number.Number) or isinstance(x, Complex.Complex):
            new_m = Matrix(self.variables, self.functions)
            for i, row in enumerate(self.data):
                tmp = []
                for j, item in enumerate(row):
                    tmp.append(self.data[i][j] % x)
                new_m.add_row(tmp)
            return new_m
        else:
            raise InputSyntaxException('Error: You can\'t do this operation with Matrix and {0}'.format(type(x).__name__))

    def __pow__(self, x):
        if not isinstance(x, Number.Number) or x % Number.Number(1) or x < Number.Number(0):
            raise InputSyntaxException('Error: Power should be positive integer or zero, {0} given'.format(x))
        if x == 0:
            return Number.Number(1)
        elif x == 1:
            return self
        else:
            result = self
            while x != 1:
                result *= self
                x -= Number.Number(1)
            return result
        
    def __str__(self):
        result = []
        for lst in self.data:
            result.append('[{0}]'.format(','.join(map(str,lst))))
        return "\n".join(result)

    def __eq__(self, x):
        if isinstance(x, Matrix):
            if x.rows != self.rows or x.columns != self.columns:
                return False
            for i, row in enumerate(self.data):
                for j, item in enumerate(self.data):
                    if self.data[i][j] != x.data[i][j]:
                        return False
            return True
        else:
            return False

    # def __repr__(self):
    #     return self.string

if __name__ == '__main__':
    # m1 = Matrix({}, {})
    # m1.string = "[[22,1,123,555];[0,-2,110,10];[12,101,3,4];[2,-1,2,3]]"
    # m1.string = "[[4,3];[3,2]]"
    # m1.string = "[[13,26];[39,13]]"
    # m1.parse_string()


    # m2 = Matrix({}, {})
    # m2.string = "[[7,4];[2,3]]"
    # m2.parse_string()

    x = Number.Number("-0")
    # print()
    # print(m2)
    # print()
    # print(m2 / m1)