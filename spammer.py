import keyboard
from time import sleep

while True:
    if keyboard.is_pressed('ctrl'):
        break
for i in range(100):
    if keyboard.is_pressed('s'):
        break
    keyboard.press("ctrl")
    keyboard.press_and_release('v')
    keyboard.release('ctrl')
    keyboard.press('enter')
    sleep(2)