import re
import math

class Calculator:

    pattern = re.compile(r'^[e.()\s\d+*/-]*$')

    def eval(self, expr: str):
        if expr[-1] != '=':
            raise ValueError("expect '=' terminator")
        expr = expr[:-1]
        if not self.pattern.match(expr):
            raise ValueError(f'invalid expression: {repr(expr)}')
        try:
            value = eval(expr)  # it's dangeous but we like this...
        except Exception:  # e.g., ZeroDivisionError, SyntaxError...
            value = math.nan
        return value, self.format(value)

    def format(self, value):
        if type(value) is int:
            return '%d' % value
        elif type(value) is float:
            return '%g' % value
        else:  # the program may better crash if an unexpected type got...
            raise ValueError(f'invalid value type: {repr(type(value))}')

if __name__ == '__main__':
    calc = Calculator()
    print(calc.eval('1 ='))
    print(calc.eval('1e8 ='))
    print(calc.eval('1 + 1 ='))
    print(calc.eval('1 + 2 ='))
    print(calc.eval('1 - 2 ='))
    print(calc.eval('1 * 2 ='))
    print(calc.eval('1 / 2 ='))
    print(calc.eval('1 + 2 * 4 ='))
    print(calc.eval('(1 + 2) * 4 ='))
    print(calc.eval('((1 + 2) * 4 ='))
    print(calc.eval('3 / 0 ='))
    print(calc.eval('3.0 / 0.0 ='))
    print(calc.eval('0 / 0 ='))
    print(calc.eval('0.0 / 0.0 ='))
