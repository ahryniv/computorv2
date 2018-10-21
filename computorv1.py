import sys
import re
import Number
import InputSyntaxException
from   decimal import Decimal

class Computorv1:

    all_are_solutions = "All real numbers are solutions"

    def __init__(self, line):
        self.line = line.replace(" ", "")
        self.argument = None
        self.polynomials = dict()

    def calculate(self):
        polynomials = self.get_polynomials()
        if not self.polynomials:
            return self.all_are_solutions
        
        # Print reduced form
        # self.print_reduced_form()
        ########################

        polynomial_degree = Number.Number(max(self.polynomials))
        self.print_polynomial_degree(polynomial_degree)
        if polynomial_degree == Number.Number(2):
            solutions = self.calculate_quadratic()
            return solutions
        elif polynomial_degree == Number.Number(1):
            solution = self.calculate_simple()
            return solution
        else:
            return "Nothing to calculate"

    def get_polynomials(self):
        two_parts = self.line.split("=")
        left = two_parts[0]
        right = two_parts[1]
        self.group_polynomials(left, False)
        self.group_polynomials(right, True)

    def group_polynomials(self, line, reverse_sign_flag):
        while True:
            plus_pos = line.rfind("+")
            minus_pos = line.rfind("-")
            if plus_pos == minus_pos == -1:
                self.get_new_polynomial("+", line, reverse_sign_flag)
                break    
            elif plus_pos > minus_pos:
                tmp = line.rpartition("+")
                line = tmp[0]
            else:
                tmp = line.rpartition("-")
                line = tmp[0]
            self.get_new_polynomial(tmp[1], tmp[2], reverse_sign_flag)
        
    def get_new_polynomial(self, sign, polynomial, reverse_sign_flag):
        polynomial = polynomial.strip(" *")
        if not polynomial:
            return
        if not re.match('^([0-9]*\*?[a-z]+\^?[0-9]*)|([0-9]+)$', polynomial, re.IGNORECASE):
            raise InputSyntaxException.InputSyntaxException("Syntax error found here: {0}".format(polynomial))
        tmp = self.split_polynomial(polynomial)
        quantity = tmp[0]
        power = tmp[1]
        if Number.Number(power) > Number.Number(2):
            raise InputSyntaxException.InputSyntaxException("The polynomial degree is stricly greater than 2, I can't solve. {0}".format(power))
        if (reverse_sign_flag):
            sign = self.reverse_sign(sign)
        if not str(power) in self.polynomials:
            self.polynomials[str(power)] = Number.Number(0)
        if sign == "+":
            self.polynomials[str(power)] += quantity
        elif sign == "-":
            self.polynomials[str(power)] -= quantity
        if self.polynomials[str(power)] == Number.Number(0):
            del self.polynomials[str(power)]

    def split_polynomial(self, polynomial):

        quantity = re.search('^[0-9]*', polynomial).group(0)
        quantity = Number.Number(quantity) if quantity else Number.Number(1)

        argument = re.search('[a-zA-Z]+', polynomial)
        argument = argument if not argument else argument.group(0)
        if argument and not self.argument:
            self.argument = argument
        elif argument and self.argument and argument != self.argument:
            raise InputSyntaxException.InputSyntaxException("Unrecognized variable: {0}".format(argument))
            
        power = re.search('(?:[a-zA-Z^]+?)([0-9]*)$', polynomial)
        power = Number.Number(power.group(1)) if power and power.group(1) else \
            (Number.Number(0) if not argument else Number.Number(1))
        return quantity, power

    def calculate_quadratic(self):
        a = Number.Number(0)
        b = Number.Number(0)
        c = Number.Number(0)

        if '2' in self.polynomials:
            a = self.polynomials['2']
        if '1' in self.polynomials:
            b = self.polynomials['1']
        if '0' in self.polynomials:
            c = self.polynomials['0']
        discriminant = b ** Number.Number(2) - Number.Number(4) * a * c
        self.print_discriminant(discriminant)
        if (discriminant > 0):
            sqrt_discr = discriminant ** Number.Number(0.5)
            b = b * Number.Number(-1)
            a_a = Number.Number(2) * a
            x1 = (b + sqrt_discr) / a_a
            x2 = (b - sqrt_discr) / a_a
            return (x1, x2)
        elif (discriminant == 0):
            return ( b * Number.Number(-1) ) / ( Number.Number(2) * a )
        else:
            discriminant = ( discriminant * Number.Number(-1) ) ** Number.Number(0.5)
            imagine_part = str(discriminant) + "i"
            b = b * Number.Number(-1)
            b_2a = b / ( Number.Number(2) * a ) 
            x1 = str(b_2a) + " + " if b_2a != 0 else ""
            x1 = x1 + imagine_part
            x2 = str(b_2a) + " - " if b_2a != 0 else ""
            x2 = x2 + imagine_part
            return (x1, x2)
            
    def calculate_simple(self):
        b = Number.Number(0)
        c = Number.Number(0)

        if '1' in self.polynomials:
            b = self.polynomials['1']
        if '0' in self.polynomials:
            c = self.polynomials['0']
        return (c * Number.Number(-1)) / b

    def reverse_sign(self, sign):
        if sign == "-":
            return "+"
        return "-"

    def print_reduced_form(self):
        reduced_form = ""
        if '2' in self.polynomials:
            reduced_form += "{0:+} * X^2 ".format(self.polynomials['2'].val)
        if '1' in self.polynomials:
            reduced_form += "{0:+} * X ".format(self.polynomials['1'].val)
        if '0' in self.polynomials:
            reduced_form += "{0:+} ".format(self.polynomials['0'].val)
        if reduced_form and reduced_form[0] == "+":
            reduced_form = reduced_form[1:]
        print("Reduced form: {0}= 0".format(reduced_form))

    def print_polynomial_degree(self, polynomial_degree):
        print("Polynomial degree: {0}".format(polynomial_degree))

    def print_discriminant(self, discriminant):
        if discriminant > Number.Number(0):
            print("Discriminant is strictly positive ({0}), the two solutions are:".format(discriminant.val))
        elif discriminant == Number.Number(0):
            print("Discriminant is zero, the solution is:")
        else:
            print("Discriminant is negative({0}), two imaginary numbers are solutions".format(discriminant.val))

    # def print_solutions(self, solutions):
    #     for i in range(len(solutions)):
    #         print(solutions[i])

    def print_solution(self, solution):
        print("The solution is:")
        print(solution)




if __name__ == "__main__":
    
    comp1 = Computorv1("-21 + 3x =-x^2", {}, {})
    print(comp1.calculate())
    # comp1.get_new_polynomial({}, "+", sys.argv[1], False)