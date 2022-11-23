import os
import sys
from serial import Serial
import time

class VirtualSerial:

    # open fd=1 with write|binary|unbuffered mode
    def __init__(self, serial: Serial=None):
        self.serial = serial
        self.out = os.fdopen(1, 'wb', 0)

    # not supplied in Serial
    def _clear(self) -> None:
        if sys.platform == 'win32':
            os.system('cls')
        else:  # good luck...
            os.system('clear')

    # display bytes on the screen
    def write(self, b: bytes) -> None:
        if type(b) is not bytes:
            raise ValueError('expect bytes argument')
        self._clear()
        self.out.write(b)
        if self.serial:
            self.serial.write(b)

class Screen:

    capacity = 8  # we have 8 7-seg digit tubes...

    def __init__(self, serial: Serial=None):
        if serial is None:
            serial = VirtualSerial()
        self.serial = serial
        self.buffer = ''
        self.window = [0, 0]

    def __len__(self) -> int:
        return len(self.buffer)

    @property
    # get string content of the buffer window
    def display(self):
        l, r = self.window
        if r - l > self.capacity:
            raise OverflowError('too wide window')
        if l < 0 or r > len(self.buffer):
            raise OverflowError('window sides out of range')
        return self.buffer[l:r]

    @property
    # get bytes content of the serial output
    def output(self):
        # adding left- and right-hand-side overflow marker
        # ragged left
        return (
            ('.' if self.window[0] > 0 else '|') + \
            '%8s' % self.display + \
            ('.' if self.window[1] < len(self.buffer) else '|')
        ).encode()

    # write the buffer window to the serial
    def update(self):
        self.serial.write(self.output)

    def ragged_left(self) -> None:
        self.window[1] = len(self.buffer)
        self.window[0] = max(0, len(self.buffer) - self.capacity)
        self.update()

    def ragged_right(self) -> None:
        self.window[0] = 0
        self.window[1] = min(self.capacity, len(self.buffer))
        self.update()

    # override the buffer
    def write(self, s: str) -> None:
        self.buffer = s
        self.ragged_left()

    # get buffer content
    def read(self) -> str:
        return self.buffer

    # write at the end of the buffer
    def append(self, s: str) -> None:
        self.buffer += s
        self.ragged_left()

    def delete(self, n=1) -> bool:
        if n < 0 or n > len(self.buffer):
            return False
        self.buffer = self.buffer[:-n]
        self.ragged_left()

    # clear the buffer
    def clear(self) -> None:
        self.buffer = ''
        self.ragged_left()

    # move the window torwards left
    def left_shift(self, n: int=1) -> bool:
        if n > 0 and self.window[0] - n >= 0:
            self.window[0] -= n
            self.window[1] -= n
            self.update()
            return True
        return False

    # move the window torwards right
    def right_shift(self, n: int=1) -> bool:
        if n > 0 and self.window[1] + n <= len(self.buffer):
            self.window[0] += n
            self.window[1] += n
            self.update()
            return True
        return False

if __name__ == '__main__':
    screen = Screen()
    screen.write('Hello!')
    time.sleep(0.5)

    screen.write('0')
    time.sleep(0.5)
    screen.append('1')
    time.sleep(0.5)
    screen.append('2')
    time.sleep(0.5)

    screen.append('3')
    screen.append('4')
    screen.append('5')
    screen.append('6')
    screen.append('7')
    time.sleep(0.5)

    screen.append('8')
    time.sleep(0.5)
    screen.append('9')
    time.sleep(0.5)

    screen.left_shift()
    time.sleep(0.5)
    screen.left_shift()
    time.sleep(0.5)
    screen.left_shift()
    time.sleep(0.5)

    screen.right_shift()
    time.sleep(0.5)
    screen.right_shift()
    time.sleep(0.5)
    screen.right_shift()
    time.sleep(0.5)

    screen.clear()
    time.sleep(0.5)
    screen.append('1')
    time.sleep(0.5)
    screen.append('+')
    time.sleep(0.5)
    screen.append('1')
    time.sleep(0.5)
    screen.append('=')
    time.sleep(0.5)
    screen.append('2')
    time.sleep(0.5)

    screen.clear()
    time.sleep(0.5)
    screen.append('1')
    time.sleep(0.5)
    screen.append('+')
    time.sleep(0.5)
    screen.append('1')
    time.sleep(0.5)
    screen.delete()
    time.sleep(0.5)
    screen.append('2')
    time.sleep(0.5)
    screen.append('=')
    time.sleep(0.5)
    screen.append('3')
    time.sleep(0.5)
