import  re
from    computorv1                 import Computorv1
from    InputSyntaxException       import InputSyntaxException
from    reverse_polish_notation    import ReversePolishNotation
from    Function                   import Function
import  Matrix

variables = {}
functions = {}
service_names = {'q', 'exit', 'i', 'variables', 'history', 'hist'}
history = []

def process_line(line):
    if line.find('=') == -1:
        rpn = ReversePolishNotation(line, variables, functions)
        rpn.calculate()
        return rpn.result
    elif line.count('=') == 1:
        parts = line.split('=')
        left = parts[0]
        right = parts[1]
        if right == "?":
            rpn = ReversePolishNotation(left, variables, functions)
            rpn.calculate()
            return rpn.result
        elif line.endswith('?'):
            comp1 = Computorv1(line.strip(" ?"))
            return comp1.calculate()
        elif re.match('[a-zA-Z]+\([a-zA-Z]+\)', left):
            func_name = re.search('[a-zA-Z]+\(', left).group(0)[:-1]
            func_argument = re.search('\([a-zA-Z]+\)', left).group(0).strip(' ()')
            functions[func_name] = Function(argument = func_argument, expr = right)
            return functions
        elif not left.isalpha():
            return 'Incorrect name of variable "{0}". Should be only letters "a-zA-Z"'.format(left)
        else:
            if left.lower() in service_names:
                return "'{0}' can't be variable".format(left.lower())
            rpn = ReversePolishNotation(right, variables, functions)
            rpn.calculate()
            variables[left.lower()] = rpn.result
            return rpn.result
    else: 
        return "Wrong expression"

def main():
    while True:
        try:
            input_line = input('>> ')
            if input_line.lower() and input_line.lower() != "history" and input_line.lower() != 'hist':
                history.append(input_line)
            input_line = re.sub('[ \t\n\r\x0b\x0c]', '', input_line).lower()
            if not input_line:
                continue
            if input_line == "exit" or input_line.lower() == "q":
                print("Good bye!")
                break
            elif input_line == "variables":
                for var, value in variables.items():
                    if isinstance(value, Matrix.Matrix):
                        print("{0}: Matrix\n{1}".format(var, value))    
                    else:
                        print("{0}: {1}".format(var, value))
                continue
            elif input_line == "history" or input_line == 'hist':
                for line in history:
                    print("-- {0}".format(line))
                continue
            response = process_line(input_line)
            print(response)
        except InputSyntaxException as err:
            print(err)
        except Exception:
            print("Invalid input")

if __name__ == '__main__':
    main()