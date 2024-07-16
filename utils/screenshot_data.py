###############################################################
### VIEW DINO WEBSITE AT: offline-dino-game.firebaseapp.com ###
###     REMENBER TO USE A CHROME CORE BROWSER TO OPEN IT    ###
###############################################################

import time

import pygetwindow as gw
import pyautogui
from PIL import Image
from time import sleep
import win32gui
import threading
import numpy as np
import os


window_title = 'Dinosaur Game - Opera'  # Change this to your window's title


# Function to get the title of the active window
def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        return win32gui.GetWindowText(hwnd)
    return None


class Screenshot():
    def __init__(self, thread_no: int, interval: float, **args):
        # INIT and store values
        self.thread_no = thread_no
        self.interval = interval
        self.threads, self.start_delays = [], []
        self.output_dict = {}
        self.stop_event = threading.Event()
        self.counter, self.image_counter = 0, 0
        self.counter_lock = threading.Lock()
        print(args.values())

    # Starting
    def start(self):
        self.start_threads(num_threads=self.thread_no, sleep_interval=self.interval)
    
    # Ending threads
    def stop(self):
        self.stop_event.set()
        for thread in self.threads:
            thread.join()
    
    # Starting threads
    def start_threads(self, num_threads, sleep_interval):
        
        threads = []
        
        self.start_delays = [i * sleep_interval for i in range(num_threads)]  # Different start times
        
        for i, start_delay in enumerate(self.start_delays, start=1):
            thread = threading.Thread(target=self.capture_screenshot, args=(i, num_threads*sleep_interval, start_delay))
            thread.start()
            threads.append(thread)
        self.threads = threads
    
    # Capturing and processing --- STILL WORKING ON IT
    def capture_screenshot(self, thread_id, interval, start_delay):

        sleep(start_delay)

        while not self.stop_event.is_set():
            temp = np.append(np.array(pyautogui.screenshot(region=(left, tops[0], width, height)).convert('L')),
                             np.array(pyautogui.screenshot(region=(left, tops[1], width, height)).convert('L')))
            output = np.append(temp, np.array(pyautogui.screenshot(region=(left, tops[2], width, height)).convert('L')))
            
            # THIS IS JUST A PLACEHOLDER
            if len('1') == 1:
                print(1)


# Find the window by title
window = gw.getWindowsWithTitle(window_title)[0]

# Get the window's region (left, top, width, height)
left = window.left + 248
width = window.width - 260
height = 1
tops = [window.top + 820, window.top + 924, window.top + 1024]

counter = 0


active_window_title = get_active_window_title()
while active_window_title != window_title:
    sleep(0.01)
    counter += 1
    if (counter % 100) == 0: print('Please Open Your Screenshot Window')
    active_window_title = get_active_window_title()

# Add an interval for reaction time
sleep(3)

# Main logic
if active_window_title == window_title:
    num_threads = 10  # Adjust based on how many threads you want to use
    sleep_interval = 1.2  # The sleep interval for all threads
    Threading = Screenshot(10, 1.2)
    Threading.start()

    # Example of running threads for a certain period or condition
    try:
        while True:
            # Update `active_window_title` if needed
            active_window_title = get_active_window_title()
            if active_window_title != window_title:
                break
    finally:
        # Stop threads gracefully

        Threading.stop()
        print("Threads have been stopped.")
