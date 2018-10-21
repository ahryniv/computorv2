from    decimal                import *
from    InputSyntaxException   import InputSyntaxException
import  Matrix
import  Complex

class Number:

    def __init__(self, n):
        try:
            self.val = n.val if isinstance(n, Number) else Decimal(n)
        except InvalidOperation:
            raise InputSyntaxException('Error: Bad conversion to Decimal: {0}'.format(n))

    def __str__(self):
        val = self.val if self.val else Decimal(0)
        return str(val)

    def __repr__(self):
        return str(self.val)

    def __add__(self, x):
        if isinstance(x, Number):
            return Number(self.val + x.val)
        elif isinstance(x, Complex.Complex):
            return Complex.Complex(self, 0) + x
        elif isinstance(x, Matrix.Matrix) and self.val == 0:
            return x
        else:
            raise InputSyntaxException('Error: You can\'t add Number with {0}'.format(type(x).__name__))

    def __sub__(self, x):
        if isinstance(x, Number):
            return Number(self.val - x.val)
        elif isinstance(x, Complex.Complex):
            return Complex.Complex(self, 0) - x
        elif isinstance(x, Matrix.Matrix) and self.val == 0:
            return x * Number(-1)
        else:
            raise InputSyntaxException('Error: You can\'t subtract Number with {0}'.format(type(x).__name__))

    def __mul__(self, x):
        if isinstance(x, Number):
            return Number(self.val * x.val)
        elif isinstance(x, Matrix.Matrix):
            return x * self
        elif isinstance(x, Complex.Complex):
            return Complex.Complex(self, 0) * x
        else:
            raise InputSyntaxException('Error: You can\'t multiply Number with {0}'.format(type(x).__name__))

    def __truediv__(self, x):
        if isinstance(x, Number):
            if not x.val:
                raise InputSyntaxException("Error: Divide by zero")
            return Number(self.val / x.val)
        elif isinstance(x, Complex.Complex):
            return Complex.Complex(self, 0) / x
        else:
            raise InputSyntaxException('Error: You can\'t divide Number with {0}'.format(type(x).__name__))

    def __mod__(self, x):
        if isinstance(x, Number):
            return Number(self.val % x.val)
        elif isinstance(x, Complex.Complex):
            return Complex.Complex(self, 0) % x
        else:
            raise InputSyntaxException('Error: You can\'t divide Number with {0}'.format(type(x).__name__))

    def __pow__(self, x):
        if isinstance(x, Number):
            return Number(self.val ** x.val)
        else:
            raise InputSyntaxException('Error. Power should be Number. {0} given'.format(type(x).__name__))

    def __bool__(self):
        if self.val == 0:
            return False
        else:
            return True

    def __eq__(self, x):
        if  isinstance(x, Number):
            return self.val == x.val
        elif isinstance(x, int) or isinstance(x, float) or isinstance(x, Decimal):
            return self.val == x
        else:
            return False

    def __lt__(self, x):
        if isinstance(x, Number):
            return self.val < x.val
        elif isinstance(x, int) or isinstance(x, float) or isinstance(x, Decimal):
            return self.val < x

    def __gt__(self, x):
        if isinstance(x, Number):
            return self.val > x.val
        elif isinstance(x, int) or isinstance(x, float) or isinstance(x, Decimal):
            return self.val > x

    def __ge__(self, x):
        if isinstance(x, Number):
            return self.val >= x.val
        elif isinstance(x, int) or isinstance(x, float) or isinstance(x, Decimal):
            return self.val >= x

    def __le__(self, x):
        if isinstance(x, Number):
            return self.val <= x.val
        elif isinstance(x, int) or isinstance(x, float) or isinstance(x, Decimal):
            return self.val <= x


if __name__ == '__main__':
    n1 = Decimal(-0)
    # n2 = Number("11.2")
    # print(n1 + n2)
    # print(n1 - n2)
    # print(n1 * n2)
    # print(n1 / n2)
    # print(n1 % n2)
    # print(n1 ** n2)
    print(n1)
    # if n1 >= 0:
    #     print("true")
    # else:
    #     print("false")