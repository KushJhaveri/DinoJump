import numpy as np
import cupy as cp
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import time
import pygetwindow as gw

from time import sleep
from pynput.keyboard import Key, Controller
from screenshot_data import Screenshot

# METADATA
fps = 10
frame = 1/fps
thread = 10

window_title = 'Dinosaur Game - Opera'  # Change this to your window's title

# Find the window by title
window = gw.getWindowsWithTitle(window_title)[0]

# Get the window's region (left, top, width, height)
left = window.left + 110
width = window.width - 260
height = 1
tops = [window.top + 564, window.top + 820, window.top + 924, window.top + 1024]

score_left = 2472
score_width = 30
monitor = [
        {"top": tops[0], "left": score_left, "width": score_width, "height": 1},
        {"top": tops[1], "left": left, "width": width, "height": 1},
        {"top": tops[2], "left": left, "width": width, "height": 1},
        {"top": tops[3], "left": left, "width": width, "height": 1}
]

env = Screenshot(thread_no=thread, interval=frame, monitor=monitor, height=height, width=width)
print('loaded')
sleep(5)
keyboard = Controller()
env.start()
sleep(3.3*frame)
end = False

data = env.get_data()

while not end:
    t = time.time()

    isend = False

    while data[0] < 4:
        pass
    # print(data)
    if data[2] == -3000:
        isend = True
    if isend:
        end = True
    t = time.time() - t
    # print(t)
    sleep(frame-t)

env.stop()

# Simulate pressing the 'enter' key
keyboard.press(Key.space)
keyboard.release(Key.space)
print('HI')
# Simulate typing 'hello'
# thread_mod = Screenshot('')
