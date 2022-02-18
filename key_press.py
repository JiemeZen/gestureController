from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

time.sleep(2)

for char in "Hello World!":
    keyboard.press(char)
    keyboard.release(char)
    time.sleep(0.12)