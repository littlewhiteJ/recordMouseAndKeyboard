from pynput import mouse
from pynput import keyboard
import time
import json
import threading
import os

############################
resize_rate = 1.5
logging_file = 'log1.json'
############################

lock = threading.Lock()
logging = []
timemark = time.time()

mouse_listener = None
keyboard_listener = None


'''
# define some tag for mouse and 
mouse_move_ = 0
mouse_click_ = 1
mouse_scroll_ = 2
keyboard_press_ = 3
keyboard_release_ = 4
'''

def on_move(x, y):
    global timemark
    global logging
    
    timespan = time.time() - timemark
    lock.acquire()
    logging.append((0, timespan, int(x / resize_rate), int(y / resize_rate), 0, 0))
    lock.release()
    timemark = time.time()


def on_click(x, y, button, pressed):
    global timemark
    global logging
    
    timespan = time.time() - timemark
    lock.acquire()
    logging.append((1, timespan, int(x / resize_rate), int(y / resize_rate), 0 if button == mouse.Button.left else 1, 1 if pressed else 0))
    lock.release()
    timemark = time.time()

def on_scroll(x, y, dx, dy):
    global timemark
    global logging
    
    timespan = time.time() - timemark
    lock.acquire()
    logging.append((2, timespan, int(x / resize_rate), int(y / resize_rate), dx, dy))
    lock.release()
    timemark = time.time()

    
def on_press(key):
    global logging
    global mouse_listener
    global keyboard_listener
    if key == keyboard.Key.esc:
        # Stop listener
        mouse_listener.stop()
        keyboard_listener.stop()
        print('stop')
        with open(logging_file, 'w') as logfile:
            json.dump(logging, logfile)
        os._exit(0)
        
    # print(key.value.vk)
    global timemark
    
    timespan = time.time() - timemark
    lock.acquire()
    try:
        logging.append((3, timespan, key.vk, 0, 0, 0))
    except:
        logging.append((3, timespan, key.value.vk, 0, 0, 0))
    lock.release()
    timemark = time.time()


def on_release(key):
    global logging
    global timemark
    
    timespan = time.time() - timemark
    lock.acquire()
    try:
        logging.append((4, timespan, key.vk, 0, 0, 0))
    except:
        logging.append((4, timespan, key.value.vk, 0, 0, 0))
    lock.release()
    timemark = time.time()
    
'''
# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
        ) as keyboard_listener:
    keyboard_listener.join()
''' 

def start_record():
    global logging
    global mouse_listener
    global keyboard_listener
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()
    print(keyboard_listener)
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    mouse_listener.start()
    
    mouse_listener.join()
    keyboard_listener.join()
    

if __name__ == '__main__':
    start_record()
