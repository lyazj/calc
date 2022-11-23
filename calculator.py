import re
from math import nan, inf  # for eval

class Calculator:

    # not rigorous, but maybe very useful for debugging...
    pattern = re.compile(r'^(?:[.()\s\d+*/-]|\b(?:nan|inf)\b|[0-9.][e|E][-+0-9])*$')

    def __init__(self):
        self.history = []

    def eval(self, expr: str) -> str:
        if expr[-1] != '=':
            raise ValueError("expect '=' terminator")
        if expr.find('=') == len(expr) - 1:
            ex = expr[:-1]
            if not self.pattern.match(ex):
                raise ValueError(f'invalid expression: {repr(expr)}')
            try:
                value = eval(ex)  # it's dangeous but we like this...
            except Exception:  # e.g., ZeroDivisionError, SyntaxError...
                value = nan
        else:
            value = nan
        value = self.format(value)
        expr += value
        self.history.append((expr, value))
        return value

    def format(self, value: int or float) -> str:
        if type(value) is int:
            return '%d' % value
        elif type(value) is float:
            return '%g' % value
        else:  # the program may better crash if an unexpected type got...
            raise ValueError(f'invalid value type: {repr(type(value))}')

if __name__ == '__main__':
    calc = Calculator()
    print(calc.eval('='))
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
