from pynput.mouse import Button
from pynput import mouse
from pynput import keyboard
from pynput.keyboard import KeyCode
import json
import time
import os

############################
resize_rate = 1.5
logging_file = 'log1.json'
############################

mouse = mouse.Controller()
keyboard = keyboard.Controller()

def move(x, y):
    mouse.position = (x, y)
    
def click(x, y, left_button, pressed):
    mouse.position = (x, y)
    if left_button == 0 and pressed:
        mouse.press(Button.left)
    elif left_button == 0 and not pressed:
        mouse.release(Button.left)
    elif left_button == 1 and pressed:
        mouse.press(Button.right)
    elif left_button == 1 and not pressed:
        mouse.release(Button.right)

def scroll(dx, dy):
    mouse.scroll(dx, dy)
    
def press(key):
    keyboard.press(KeyCode.from_vk(int(key)))
    
def release(key):
    keyboard.release(KeyCode.from_vk(int(key)))
    
    

    
with open(logging_file, 'r') as logfile:
    logging = json.load(logfile)

for tag, timespan, x, y, xx, yy in logging:
    if tag == 0: # mouse move
        time.sleep(timespan)
        move(x, y)
    elif tag == 1: # mouse click
        time.sleep(timespan)
        click(x, y, xx, yy)
    elif tag == 2: # mouse scroll
        time.sleep(timespan)
        scroll(xx, yy)
    elif tag == 3: # keyboard press
        time.sleep(timespan)
        press(x)
    elif tag == 4: # keyboard release
        time.sleep(timespan)
        release(x)

os._exit(0) 

