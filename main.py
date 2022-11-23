from calculator import Calculator
from screen import Serial, VirtualSerial, Screen
from window import Window
from getpass import getuser

# configuration
port = None
virtual = True
virtualOnly = True  # False on release

# object constructions
calculator = Calculator()
if virtualOnly:
    virtual = True
    serial = None
else:
    port = port if port else '/dev/ttyUSB0' if getuser() == 'lyazj' else input('port: ')
    serial = Serial(port, 115200, timeout=0)
virtualSerial = serial if not virtual else VirtualSerial(serial)
screen = Screen(virtualSerial)
window = Window(calculator, screen)

if __name__ == '__main__':
    window.loop()
