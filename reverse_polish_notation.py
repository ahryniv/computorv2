import  re
import  operator
from    InputSyntaxException   import InputSyntaxException
from    decimal                import Decimal
import  Complex
import  Matrix
import  Number

class ReversePolishNotation:
    operators = {
        '(': 0,
        ')': 1,
        '-': 2,
        '+': 2,
        '*': 3,
        '/': 3,
        '%': 3,
        '^': 4
    }
    ops = {
        "+": operator.add, 
        "-": operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '%': operator.mod,
        '^': operator.pow
    }

    def __init__(self, line, vars, funcs):
        self.vars = vars
        self.funcs = funcs
        self.line = line
        self.output = []
        self.stack = []
        self.matrix_checker = 0
        self.result = None
                
    def convert(self):
        operand = ""
        func = False
        matrix = None
        for index, char in enumerate(self.line):
            if func:
                operand += char
                if char == ')':
                    func = False
            elif self.matrix_checker:
                self.add_symbol_to_matrix(char, matrix)
            elif char == '[':
                if operand:
                    raise InputSyntaxException('Syntax error found here: "{0}"'.format(self.line))
                self.matrix_checker += 1
                matrix = Matrix.Matrix(self.vars, self.funcs)
                matrix.add_symbol(char)
            elif char in "-+*/%^":
                if not operand and char == '-' and self.line[index + 1].isdigit():
                    operand += char
                    continue
                if operand:
                    operand = self.add_operand(operand)
                self.add_to_stack(char)
            elif char == "(":
                if operand and operand in self.funcs.keys():
                    operand += char
                    func = True
                    continue
                self.stack.append(char)
            elif char == ")":
                if operand:
                    operand = self.add_operand(operand)
                self.add_to_stack(char)
            elif char.isalnum() or char == '.':
                operand += char
            else:
                raise InputSyntaxException('Syntax error found here: "{0}", unknown char "{1}"'.format(self.line, char))
        if operand:
            operand = self.add_operand(operand)
        while self.stack:
            el = self.stack.pop()
            if el == "(":
                raise InputSyntaxException('Parentheses error in "{0}"'.format(self.line))
            self.output.append(el)

    def add_operand(self, operand):
        if not self.allowed_operand(operand):
            raise InputSyntaxException('Syntax error found here: "{0}", Operand: "{1}"'.format(self.line, operand))
        if isinstance(operand, Matrix.Matrix):
            self.output.append(operand)
        elif operand.lower() in self.vars.keys():
            self.output.append(self.vars[operand.lower()])
        elif self.isimaginary(operand):
            im = operand[:-1]
            im = im if im else 1
            self.output.append( Complex.Complex(0, im))
        elif self.isfunc(operand):
            func_name = re.search('[a-zA-Z]+\(', operand).group(0)[:-1]
            func_argument = re.search('\(.+\)', operand).group(0).strip(' ()')
            if func_name in self.funcs.keys():
                rpn = ReversePolishNotation(func_argument, self.vars, self.funcs)
                rpn.calculate()
                func_argument = rpn.result
                self.output.append(self.funcs[func_name].calculate(func_argument, self.funcs, self.vars))
            else:
                raise InputSyntaxException('Unrecognized function "{0}"'.format(operand))
        elif self.isfloat(operand):
            self.output.append(Number.Number(operand))
        else:
            raise InputSyntaxException('Unrecognized variable "{0}"'.format(operand))
        operand = ""
        return operand

    def add_symbol_to_matrix(self, char, matrix):
        matrix.add_symbol(char)
        if char == ']':
            self.matrix_checker -= 1
        elif char == '[':
            self.matrix_checker += 1
        if self.matrix_checker == 0:
            matrix.parse_string()
            self.add_operand(matrix)

    def add_to_stack(self, operator):
        try:
            while self.stack and self.operators[self.stack[-1]] >= self.operators[operator]:
                self.output.append(self.stack.pop())
            if self.stack and operator == ")" and self.stack[-1] == "(":
                self.stack.pop()
            if operator != ")":
                self.stack.append(operator)
        except IndexError:
            raise InputSyntaxException('Parentheses error in "{0}"'.format(self.line))

    def calculate(self):
        assert not self.stack, "Stack should be empty"
        self.output = []
        self.convert()
        try:
            for i in self.output:
                if str(i) not in "-+*/%^":
                    self.stack.append(i)
                else:
                    arg2 = self.stack.pop()
                    arg1 = self.stack.pop()
                    result = self.ops[i](arg1, arg2)
                    self.stack.append(result)
            self.result = self.stack[0]
        except IndexError:
            raise InputSyntaxException('Syntax error found here: "{0}"'.format(self.line))

    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def isfunc(self, operand):
        # if re.match('[a-zA-Z]+\([a-zA-Z0-9.]+\)', operand):
        if re.match('[a-zA-Z]+\(.+\)', operand):
            return True
        return False

    def isimaginary(self, operand):
        if not operand.endswith('i'):
            return False
        if operand == 'i':
            return True
        operand = operand[:-1]
        if operand.isdigit():
            return True
        if operand.isalpha():
            return True
        if self.isfloat(operand):
            return True
        return False

    def allowed_operand(self, operand):
        if not operand:
            return False
        if isinstance(operand, Matrix.Matrix):
            return True
        if operand.isdigit():
            return True
        if operand.isalpha():
            return True
        if self.isfloat(operand):
            return True
        if self.isfunc(operand):
            return True
        if self.isimaginary(operand):
            return True
        return False
