from pynput.mouse import Button
from pynput import mouse
from pynput import keyboard
from pynput.keyboard import KeyCode
import json
import time
import os

class Replaying:
    def __init__(self):
        self.mouse = mouse.Controller()
        self.keyboard = keyboard.Controller()
    
    def move(self, x, y):
        self.mouse.position = (x, y)

    def click(self, x, y, leftButton, pressed):
        self.mouse.position = (x, y)
        if leftButton == 0 and pressed:
            self.mouse.press(Button.left)
        elif leftButton == 0 and not pressed:
            self.mouse.release(Button.left)
        elif leftButton == 1 and pressed:
            self.mouse.press(Button.right)
        elif leftButton == 1 and not pressed:
            self.mouse.release(Button.right)
    def scroll(self, dx, dy):
        self.mouse.scroll(dx, dy)
    
    def press(self, key):
        self.keyboard.press(KeyCode.from_vk(int(key)))

    def release(self, key):
        self.keyboard.release(KeyCode.from_vk(int(key)))
    
    def startReplay(self, logFile):
        with open(logFile, 'r') as f:
            logs = json.load(f)
        
        # print('Start Replay')
        for tag, timespan, x, y, xx, yy in logs:
            if tag == 0: # mouse move
                time.sleep(timespan)
                self.move(x, y)
            elif tag == 1: # mouse click
                time.sleep(timespan)
                self.click(x, y, xx, yy)
            elif tag == 2: # mouse scroll
                time.sleep(timespan)
                self.scroll(xx, yy)
            elif tag == 3: # keyboard press
                time.sleep(timespan)
                self.press(x)
            elif tag == 4: # keyboard release
                time.sleep(timespan)
                self.release(x)

        # print('End Replay')
        # os._exit(0)
