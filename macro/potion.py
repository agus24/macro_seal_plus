from datetime import datetime, timedelta

import keyboard
import pywinauto as p
import pyautogui
from core.exceptions import ExitMenuException


class Potion:
    def __init__(self):
        self.keyboard = p.keyboard


    def start_potion_2(self):
        pyautogui.press('F1')
        pyautogui.press('F2')
        pyautogui.press('F3')
        pyautogui.press('F4')
        pyautogui.press('F5')
        pyautogui.press('F6')
        pyautogui.press('F7')
        pyautogui.press('F8')
        pyautogui.press('F9')
        pyautogui.press('F10')

        pyautogui.press('3')
        pyautogui.press('4')
        pyautogui.press('5')
        pyautogui.press('6')
        pyautogui.press('7')
        pyautogui.press('8')
        pyautogui.press('9')
        pyautogui.press('0')

        pyautogui.press('TAB')

        pyautogui.press('F1')
        pyautogui.press('F2')
        pyautogui.press('F3')
        pyautogui.press('F4')
        pyautogui.press('F5')
        pyautogui.press('F6')
        pyautogui.press('F7')
        pyautogui.press('F8')
        pyautogui.press('F9')
        pyautogui.press('F10')

    def start_potion(self):
        self.keyboard.send_keys('{F1}')
        self.keyboard.send_keys('{F2}')
        self.keyboard.send_keys('{F3}')
        self.keyboard.send_keys('{F4}')
        self.keyboard.send_keys('{F5}')
        self.keyboard.send_keys('{F6}')
        self.keyboard.send_keys('{F7}')
        self.keyboard.send_keys('{F8}')
        self.keyboard.send_keys('{F9}')
        self.keyboard.send_keys('{F10}')

        self.keyboard.send_keys( '{3 down}' '{3 up}' )
        self.keyboard.send_keys( '{4 down}' '{4 up}' )
        self.keyboard.send_keys( '{5 down}' '{5 up}' )
        self.keyboard.send_keys( '{6 down}' '{6 up}' )
        self.keyboard.send_keys( '{7 down}' '{7 up}' )
        self.keyboard.send_keys( '{8 down}' '{8 up}' )
        self.keyboard.send_keys( '{9 down}' '{9 up}' )
        self.keyboard.send_keys( '{0 down}' '{0 up}' )

        self.keyboard.send_keys('{TAB}')

        self.keyboard.send_keys('{F1}')
        self.keyboard.send_keys('{F2}')
        self.keyboard.send_keys('{F3}')
        self.keyboard.send_keys('{F4}')
        self.keyboard.send_keys('{F5}')
        self.keyboard.send_keys('{F6}')
        self.keyboard.send_keys('{F7}')
        self.keyboard.send_keys('{F8}')
        self.keyboard.send_keys('{F9}')
        self.keyboard.send_keys('{F10}')

    def start(self):
        print('starting')
        while True:
            if keyboard.is_pressed('`'):
                self.start_potion()
            34567890
            if keyboard.is_pressed('ctrl'):
                if keyboard.is_pressed('='):
                    raise ExitMenuException
                    return
