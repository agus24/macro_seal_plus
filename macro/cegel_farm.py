from datetime import datetime, timedelta
import keyboard
import pywinauto as p
from time import sleep

from core import macro
from core import seal
from core.logger import Logger
from core.constants import *
from core.exceptions import ExitMenuException


class CegelFarm():
    def __init__(self):
        print("cegelcmd.py")
        self.inventory = []
        self.keyboard = p.keyboard
        self.target = 0
        self.targets = []
        self.current_target = 0
        self.force_stop = False
        self.next_buff_time = datetime.now()
        self.click_interval = datetime.now()

        self.user_id = seal.getUserId()
        self.logger = Logger(self.user_id, "cegelcmd_")

        self.logger.log("Starting Cegel Hunt")

    def check_click_gap(self, interval):
        self.current_time = datetime.now()
        if self.current_time > self.click_interval:
            self.click_interval = self.current_time + timedelta(seconds=interval)
            print("click_interval")
            return True

        return False

    def sellItem(self):
        self.logger.log("Selling Item")
        seal.moveMouse(530, 461)
        sleep(0.5)
        macro.mouseClick()
        sleep(1)
        self.keyboard.send_keys('{ENTER}')
        seal.moveMouse(*REFINE_OK_CONFIRM)
        sleep(0.5)
        macro.mouseClick()
        sleep(0.5)
        sleep(0.5)
        macro.sellSlot1()
        macro.sellSlot2()
        macro.sellSlot3()
        macro.sellSlot4()
        macro.sellSlot5()
        sleep(1)
        self.logger.log("escape")

    def buyPotion(self):
        self.logger.log("buying potion")
        seal.moveMouse(530, 461)
        sleep(0.5)
        macro.mouseClick()
        sleep(1)
        self.keyboard.send_keys('{ENTER}')
        seal.moveMouse(*REFINE_OK_CONFIRM)
        sleep(1)
        macro.buyPot()
        sleep(0.1)
        self.logger.log("bank : " + str(macro.checkBank()))
        self.logger.log("shop : " + str(macro.checkShop()))
        sleep(0.1)

    def close_if_shop_open(self):
        while seal.get_freeze_dialog() == DIALOG['shop']:
            macro.moveMouse(257, 87)
            sleep(0.2)
            macro.mouseClick()

    def need_buff(self):
        current_time = datetime.now()
        if self.next_buff_time <= current_time:
            self.next_buff_time = datetime.now() + timedelta(hours=1)
            return True
        
        return False

    def run_cegel(self):
        self.close_if_shop_open()
        target = seal.getCurrentTargetArrow()

        if target == -1:
            print("setting target")
            seal.setTarget(self.targets[self.current_target])
            self.current_target = self.current_target + 1 if self.current_target + 1 < len(self.targets) else 0

            seal.moveMouse(392, 357)
            macro.mouseClick()
            print("target : " + str(target))

        if self.check_click_gap(5):
            seal.moveMouse(392, 357)
            macro.mouseClick()

        if target:
            # self.logger.log(f"target : {str(target)}")
            if self.need_buff():
                self.logger.log("Use Buff")
                self.keyboard.send_keys('{1 down}' '{1 up}')
                sleep(1)
                self.keyboard.send_keys('{2 down}' '{2 up}')
                sleep(1)
                self.keyboard.send_keys('{3 down}' '{3 up}')
                sleep(1)
                self.keyboard.send_keys('{4 down}' '{4 up}')
                sleep(1)
                self.keyboard.send_keys('{5 down}' '{5 up}')
                sleep(1)
                return

            inventory = seal.getItemValue()
            self.keyboard.send_keys('{SPACE}')
            self.keyboard.send_keys('{F1}')
            self.keyboard.send_keys('{F2}')
            self.keyboard.send_keys('{F3}')
            self.keyboard.send_keys('{F5}')
            self.keyboard.send_keys('{F6}')
            self.keyboard.send_keys('{F7}')
            self.keyboard.send_keys('{F8}')
            self.keyboard.send_keys('{SPACE}')
            self.keyboard.send_keys('{SPACE}')

        if inventory[32]['qty'] < 150 or inventory[33]['qty'] < 150:
            self.buyPotion()
            sleep(0.5)
        for i in range(0, 8):
            if inventory[i]['qty'] >= 900:
                self.logger.log('Item > 900.')
                self.logger.log('Selling Item.')
                self.sellItem()
                self.logger.log("Hunt Continue..")
        if keyboard.is_pressed('c'):
            self.logger.log('stopping.')
            self.force_stop = True

    def print_hotkey(self):
        hotkey = [
            "[CTRL + -] START MACRO",
            "[CTRL + =] EXIT",
            "[-] SHOW CURRENT TARGET",
            "[/] REGISTER TARGET",
            "[.] RESET TARGET"
        ]
        print("\n".join(hotkey))

    def start(self):
        while True:
            if keyboard.is_pressed('ctrl'):
                if keyboard.is_pressed('-'):
                    if not len(self.targets):
                        print("Failed to start macro: Target is empty")
                        sleep(0.2)
                        return

                    self.logger.log("Start Cegel Hunt..")
                    self.force_stop = False
                    print("Targets: " + str(self.targets))
                    print("Hold c to stop hunting")
                    while True:
                        if self.force_stop:
                            break
                        self.run_cegel()
                        sleep(0.5)

                if keyboard.is_pressed('='):
                    self.logger.log('Script Stopped.')
                    raise ExitMenuException
                    return

            if keyboard.is_pressed("-"):
                print(str(self.targets))
                sleep(0.2)

            if keyboard.is_pressed("/"):
                self.logger.log(seal.getCurrentTarget())
                target = seal.getCurrentTarget()
                if target and target not in self.targets:
                    self.targets.append(target)

                self.logger.log(self.targets)
                sleep(0.2)

            if keyboard.is_pressed('.'):
                self.targets = []
                self.logger.log("Reseting Target")
                sleep(0.2)
