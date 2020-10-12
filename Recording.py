from pynput import mouse
from pynput import keyboard
import time
import json
import threading
import os

'''
# define some tag for mouse and 
mouse_move_ = 0
mouse_click_ = 1
mouse_scroll_ = 2
keyboard_press_ = 3
keyboard_release_ = 4
'''

class Recording:
    def __init__(self):
        self.resizeRate = 1.25
        self.logFile = None
        self.lock = threading.Lock()
        self.logs = []
        self.timeMark = time.time()
        self.mouseListener = None
        self.keyboardListener = None

    def onPress(self, key):
        if key == keyboard.Key.esc:
            # Stop listener
            self.mouseListener.stop()
            self.keyboardListener.stop()
            print('stop')
            with open(self.logFile, 'w') as f:
                json.dump(self.logs, f)
            os._exit(0)
        
        timespan = time.time() - self.timeMark
        self.lock.acquire()
        try:
            self.logs.append((3, timespan, key.vk, 0, 0, 0))
        except:
            self.logs.append((3, timespan, key.value.vk, 0, 0, 0))
        self.lock.release()
        self.timeMark = time.time()

    def onRelease(self, key):
        timespan = time.time() - self.timeMark
        self.lock.acquire()
        try:
            self.logs.append((4, timespan, key.vk, 0, 0, 0))
        except:
            self.logs.append((4, timespan, key.value.vk, 0, 0, 0))
        self.lock.release()
        self.timeMark = time.time()

    def onMove(self, x, y):
        timespan = time.time() - self.timeMark
        self.lock.acquire()
        self.logs.append((0, timespan, int(x / self.resizeRate), int(y / self.resizeRate), 0, 0))
        self.lock.release()
        self.timeMark = time.time()

    def onClick(self, x, y, button, pressed):
        timespan = time.time() - self.timeMark
        self.lock.acquire()
        self.logs.append((1, timespan, int(x / self.resizeRate), int(y / self.resizeRate), 0 if button == mouse.Button.left else 1, 1 if pressed else 0))
        self.lock.release()
        self.timeMark = time.time()

    def onScroll(self, x, y, dx, dy):
        timespan = time.time() - self.timeMark
        self.lock.acquire()
        self.logs.append((2, timespan, int(x / self.resizeRate), int(y / self.resizeRate), dx, dy))
        self.lock.release()
        self.timeMark = time.time()

    def startRecord(self, logFile):
        self.logFile = logFile
        self.keyboardListener = keyboard.Listener(on_press=self.onPress, on_release=self.onRelease)
        self.keyboardListener.start()
        print(self.keyboardListener)
        self.mouseListener = mouse.Listener(on_move=self.onMove, on_click=self.onClick, on_scroll=self.onScroll)
        self.mouseListener.start()
        
        self.mouseListener.join()
        self.keyboardListener.join()