import reverse_polish_notation
from InputSyntaxException import InputSyntaxException

class Function:

    def __init__(self, argument, expr):
        self.argument = argument
        self.expr = expr

    def calculate(self, var, funcs, variables):
        variables_tmp = dict(variables)
        variables_tmp[self.argument] = var
        rpn = reverse_polish_notation.ReversePolishNotation(self.expr, variables_tmp, funcs)
        rpn.calculate()
        return rpn.result