from InputSyntaxException   import InputSyntaxException
import reverse_polish_notation as rpn
import Number
import Matrix

class Complex:

    def __init__(self, re, im):
        self.re = Number.Number(re)
        self.im = Number.Number(im) if im else Number.Number(0)

    def __str__(self):
        result = ""
        sign = "+" if self.im >= Number.Number(0) else "-"
        if self.re:
            result += str(self.re)
        if len(result) != 0 and sign != "-":
            result += str(sign)
        result += str(self.im) + "i" if self.im != Number.Number(1) else "i"
        return result

    def __add__(self, x):
        if isinstance(x, Complex):
            re = self.re + x.re
            im = self.im + x.im
            return Complex(re, im) if im else Number.Number(re) 
        elif isinstance(x, Number.Number):
            return Complex(self.re + x, self.im)
        else:
            raise InputSyntaxException('Error: You can\'t add Complex with {0}'.format(type(x).__name__))

    def __sub__(self, x):
        if isinstance(x, Complex):
            re = self.re - x.re
            im = self.im - x.im
            return Complex(re, im) if im else Number.Number(re)
        elif isinstance(x, Number.Number):
            return Complex(self.re - x, self.im)
        else:
            raise InputSyntaxException('Error: You can\'t subtract Complex with {0}'.format(type(x).__name__))

    def __mul__(self, x):
        if isinstance(x, Complex):
            re = (self.re * x.re) - (self.im * x.im)
            im = (self.re * x.im) + (self.im * x.re)
            return Complex(re, im) if im else Number.Number(re)
        elif isinstance(x, Number.Number):
            re = self.re * x
            im = self.im * x
            return Complex(re, im) if im else Number.Number(re)
        elif isinstance(x, Matrix.Matrix):
            return x * self
        else:
            raise InputSyntaxException('Error: You can\'t multiply Complex with {0}'.format(type(x).__name__))

    def __truediv__(self, x):
        if isinstance(x, Complex):
            re = ((self.re * x.re) + (self.im * x.im)) / (x.re ** Number.Number(2) + x.im ** Number.Number(2))
            im = ((self.im * x.re) - (self.re * x.im)) / (x.re ** Number.Number(2) + x.im ** Number.Number(2))
            return Complex(re, im) if im else Number.Number(re)
        elif isinstance(x, Number.Number):
            re = self.re / x
            im = self.im / x
            return Complex(re, im) if im else Number.Number(re)
        else:
            raise InputSyntaxException('Error: You can\'t divide Complex with {0}'.format(type(x).__name__))

    def __mod__(self, x):
        if isinstance(x, Complex):
            re = ((self.re * x.re) + (self.im * x.im)) % (x.re ** Number.Number(2) + x.im ** Number.Number(2))
            im = ((self.im * x.re) - (self.re * x.im)) % (x.re ** Number.Number(2) + x.im ** Number.Number(2))
            return Complex(re, im) if im else Number.Number(re)
        elif isinstance(x, Number.Number):
            re = self.re % x
            im = self.im % x
            return Complex(re, im) if im else Number.Number(re)
        else:
            raise InputSyntaxException('Error: You can\'t divide Complex with {0}'.format(type(x).__name__))

    def __pow__(self, x):
        if not isinstance(x, Number.Number) or x % Number.Number(1) or x < Number.Number(0):
            raise InputSyntaxException('Error: Power should be positive Number or zero, {0} given ({1})'.format(x, type(x).__name__))
        x = Number.Number(x)
        if x == Number.Number(0):
            return Number.Number(1)
        elif x == Number.Number(1):
            return self
        elif self.re == Number.Number(0):
            remain = x % Number.Number(4)
            if remain == Number.Number(1):
                return Complex(0, self.im ** x)
            elif remain == Number.Number(2):
                return Number.Number(-1) * (self.im ** x)
            elif remain == Number.Number(3):
                return Complex(0, (self.im ** x) * Number.Number(-1) )
            else:
                return Number.Number(self.im ** x)
        else:
            sign = "+" if self.im >= 0 else "-"
            expr = ["(" + str(self.re) + sign + str(self.im) + "i)"] * int(x.val)
            expr = "*".join(expr)
            r = rpn.ReversePolishNotation(expr, {}, {})
            r.calculate()
            return r.result




if __name__ == '__main__':
    c = Complex(4,5)
    x = Complex(-1,-1123)
    print(x)
