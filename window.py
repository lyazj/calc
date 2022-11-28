from calculator import Calculator
from screen import Screen
import time

import tkinter as tk

class Window:
    # TODO: draw buttons: 0123456789.e+-*/()=ABCUDLRN

    def __init__(self, calculator: Calculator, screen: Screen):
        self.calculator = calculator
        self.screen = screen
        self.value = None   # current evaluation result
        self.cursor = 0     # current traceback position
        self.buffer = None  # saved screen buffer while looking backwards
        self.width = 800
        self.height = 600
        self.tk = None
        self.init_window()
        self.labels = None
        self.buttons = None
        self.init_components()

    def init_window(self) -> None:
        self.tk = tk.Tk()
        self.tk.title('calc')
        self.tk.geometry(f'{self.width}x{self.height}')

    def create_button(self, c: str) -> tk.Button:
        return tk.Button(
            self.tk, text=c, command=lambda: self.click(c)
        )

    def create_label(self, t: str) -> tk.Label:
        return tk.Label(
            self.tk, text=t
        )

    def init_components(self) -> None:
        self.labels = {}
        self.buttons = {}
        for t in 'Input', 'Control':
            self.labels[t] = self.create_label(t)
        for c in '0123456789.e+-*/()=ABCUDLRN':
            self.buttons[c] = self.create_button(c)
        self.labels['Input'].place(x=80, y=40)
        self.place_array(
            ['123', '456', '789', 'e0.', '+-*', '/()'],
            80, 100, 0.1, 0.1, 0.025, 0.025
        )
        self.place_array(
            ['LRN', 'UDA', "BC="],
            430, 325, 0.1, 0.1, 0.025, 0.025
        )

    def place_array(self, a, x0, y0, rw, rh, mw, mh):
        # r: relevant  m: relevant margin
        for i, ai in enumerate(a):
            for j, c in enumerate(ai):
                self.buttons[c].place(
                    x=x0 + j * (rw + mw) * self.width,
                    y=y0 + i * (rh + mh) * self.height,
                    relwidth=rw, relheight=rh
                )

    def loop(self) -> None:
        self.tk.mainloop()

    # NOTE: It may take ~100 ms for the device to response,
    #       so it's better to sleep(0.5) after each transcation.
    def test(self) -> None:
        self.click('1')
        time.sleep(0.5)
        self.click('+')
        time.sleep(0.5)
        self.click('2')
        time.sleep(0.5)
        self.click('=')
        time.sleep(1)

        self.click('C')
        time.sleep(0.5)
        self.click('A')
        time.sleep(0.5)
        self.click('+')
        time.sleep(0.5)
        self.click('2')
        time.sleep(0.5)
        self.click('B')
        time.sleep(0.5)
        self.click('3')
        time.sleep(0.5)
        self.click('=')
        time.sleep(1)

        self.click('U')
        time.sleep(0.5)
        self.click('U')
        time.sleep(0.5)
        self.click('U')
        time.sleep(0.5)
        self.click('U')
        time.sleep(0.5)
        self.click('D')
        time.sleep(0.5)
        self.click('D')
        time.sleep(0.5)
        self.click('D')
        time.sleep(0.5)
        self.click('B')
        time.sleep(0.5)
        self.click('B')
        time.sleep(0.5)
        self.click('*')
        time.sleep(0.5)
        self.click('2')
        time.sleep(0.5)
        self.click('=')
        time.sleep(0.5)

        self.click('C')
        time.sleep(0.5)
        self.click('(')
        time.sleep(0.5)
        self.click('1')
        time.sleep(0.5)
        self.click('U')
        time.sleep(0.5)
        self.click('U')
        time.sleep(0.5)
        self.click('N')
        time.sleep(0.5)
        self.click('+')
        time.sleep(0.5)
        self.click('2')
        time.sleep(0.5)
        self.click(')')
        time.sleep(0.5)
        self.click('*')
        time.sleep(0.5)
        self.click('3')
        time.sleep(0.5)
        self.click('=')
        time.sleep(0.5)
        self.click('L')
        time.sleep(0.5)
        self.click('L')
        time.sleep(0.5)
        self.click('R')
        time.sleep(0.5)
        self.click('R')
        time.sleep(0.5)

    def click(self, c: str) -> None:
        if len(c) != 1:
            raise ValueError(f'invalid button: {repr(c)}')
        if c == 'A':  # Auto
            return self.complement()
        if c == 'B':  # Backspace
            return self.delete()
        if c == 'C':  # Clear
            return self.clear()
        if c == 'U':  # Up
            return self.lookup()
        if c == 'D':  # Down
            return self.lookdown()
        if c == 'L':  # Left
            return self.screen.left_shift()
        if c == 'R':  # Right
            return self.screen.right_shift()
        if c == 'N':  # Normal
            return self.restore()
        return self.input(c)

    # do auto complement
    def complement(self) -> None:
        self.leave()
        if self.value is not None:
            self.screen.append(self.value)

    # input a character
    def input(self, c: str) -> None:
        if len(c) != 1 or c not in '0123456789.e+-*/()=':
            raise ValueError(f'invalid input: {repr(c)}')
        self.leave()
        self.screen.append(c)
        if c == '=':
            self.calculate()

    # delete a character
    def delete(self) -> None:
        self.leave()
        self.screen.delete()

    # clear the screen buffer
    def clear(self) -> None:
        self.leave()
        self.screen.clear()

    # (non-reentrant) execute expression evaluation
    # IMPORTANT: call this method only if '=' just typed by user
    def calculate(self) -> None:
        expr = self.screen.read()
        value = self.calculator.eval(expr)
        self.screen.append(value)
        self.value = value

    # (reentrant) refer to the last result
    def lookup(self) -> None:
        if self.buffer is None:  # save edited screen buffer
            self.buffer = self.screen.read()
        if self.cursor == 0:  # wrap
            self.cursor = len(self.calculator.history)
        if self.cursor == 0:  # no history
            return
        self.cursor -= 1
        expr, value = self.calculator.history[self.cursor]
        self.screen.write(expr)
        self.value = value

    # (reentrant) refer to the next result:
    def lookdown(self) -> None:
        if self.buffer is None:  # save edited screen buffer
            self.buffer = self.screen.read()
        if self.cursor == len(self.calculator.history):  # wrap
            self.cursor = 0
        if self.cursor == len(self.calculator.history):  # no history
            return
        self.cursor += 1
        expr, value = self.calculator.history[self.cursor - 1]
        self.screen.write(expr)
        self.value = value

    # (reentrant) leave traceback mode
    def leave(self) -> None:
        self.cursor = len(self.calculator.history)
        self.buffer = None

    # (reentrant) leave traceback mode and restore saved screen buffer
    def restore(self) -> None:
        if self.buffer is not None:
            self.screen.write(self.buffer)
        self.leave()
