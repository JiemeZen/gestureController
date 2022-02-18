from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller
import time

mouse = Controller()

print("Current loc:", mouse.position)

mouse.move(-2030, 1120)
time.sleep(2)
mouse.press(Button.left)
mouse.release(Button.left)
time.sleep(2)
mouse.move(1040, -540)
time.sleep(2)
mouse.position = (2040, 20)
