from datetime import datetime, timedelta
import keyboard
import pywinauto as p
from time import sleep

from core import macro
from core import seal
from core.logger import Logger
from core.constants import *
from core.exceptions import ExitMenuException

import config


class Farming():
    def __init__(self):
        print("\nGeneral Farming")
        self.inventory = []
        self.keyboard = p.keyboard
        self.target = 0
        self.targets = []
        self.current_target = 0
        self.force_stop = False
        self.next_buff_time = datetime.now()
        self.click_interval = datetime.now()

        self.click_gap = 5

        self.user_id = seal.getUserId()
        self.logger = Logger(self.user_id, "general_farming_")

        self.logger.log("Starting General Farming")

        self.excluded_items = DONT_SELL
        self.excluded_items.extend(config.dont_sell_items)

    def check_click_gap(self):
        self.current_time = datetime.now()
        if self.current_time > self.click_interval:
            self.click_interval = self.current_time + timedelta(seconds=self.click_gap)
            print("click_interval")
            return True

        return False

    def sellItem(self, slots):
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
        for slot in slots:
            macro.sell(*SHOP_INVENTORY[slot])
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
        while seal.get_dialog() == DIALOG['shop']:
            macro.moveMouse(257, 87)
            sleep(0.2)
            macro.mouseClick()

    def need_buff(self):
        current_time = datetime.now()
        if self.next_buff_time <= current_time:
            self.next_buff_time = datetime.now() + timedelta(hours=1)
            return True
        
        return False

    def start_hunt(self):
        self.close_if_shop_open()
        target = seal.getCurrentTargetArrow()

        if target == -1:
            print("setting target")
            seal.setTarget(self.targets[self.current_target])
            self.current_target = self.current_target + 1 if self.current_target + 1 < len(self.targets) else 0

            seal.moveMouse(392, 357)
            macro.mouseClick()
            print("target : " + str(target))

        if self.check_click_gap():
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

        self.check_item()
        self.check_potion()

        if keyboard.is_pressed('c'):
            self.logger.log('stopping.')
            self.force_stop = True

    def check_potion(self):
        inventory = seal.getItemValue()
        should_buy_potion = False
        for inven in inventory:
            if inven['item_id'] == POT_MERAH or inven['item_id'] == POT_BIRU:
                should_buy_potion = inven['qty'] < 150

        if should_buy_potion:
            self.logger.log("buying potion")
            self.buyPotion()
            sleep(0.5)

    def check_item(self):
        inventory = seal.getItemValue()
        should_sell = []
        prepare_sell = []
        save_to_bank = []
        for inven in inventory:
            if inven['item_id'] not in self.excluded_items:
                if inven['qty'] > 900:
                    should_sell.append(inven['slot'])

                if inven['qty'] == 0 and inven['item_id'] != 0:
                    prepare_sell.append(inven['slot'])

            if inven['item_id'] in config.should_save_to_bank:
                save_to_bank.append(inven['slot'])

        print("Prepared to bank: " + str(save_to_bank))
        print("Prepared to sell: " + str(prepare_sell))
        if len(prepare_sell) > 6:
            should_sell.extend(prepare_sell)

        print("Should Sell: " + str(should_sell))
        if should_sell:
            self.logger.log("SELL ITEM : " + str(should_sell))
            self.sellItem(should_sell)

        if len(save_to_bank) > 3:
            self.logger.log("moving_to_bank " + str(save_to_bank))
            self.move_to_bank(save_to_bank)

    def move_to_bank(self, slots):
        macro.open_bank()
        for slot in slots:
            macro.move_to_bank(slot)
        macro.close_bank()

    def print_hotkey(self):
        hotkey = [
            "\n",
            "[CTRL + -] START MACRO",
            "[CTRL + ] ] Set Multiple Target",
            "[CTRL + =] EXIT",
            "[-] SHOW CURRENT TARGET",
            "[/] REGISTER TARGET",
            "[.] RESET TARGET"
        ]
        print("\n".join(hotkey))

    def start(self):
        self.print_hotkey()
        while True:
            if keyboard.is_pressed('ctrl'):
                if keyboard.is_pressed('-'):
                    if not len(self.targets):
                        print("Failed to start macro: Target is empty")
                        sleep(0.2)
                        return

                    self.logger.log("Start General Farming..")
                    self.force_stop = False
                    print("Targets: " + str(self.targets))
                    print("Hold c to stop hunting")
                    while True:
                        if self.force_stop:
                            break
                        self.start_hunt()
                        sleep(0.5)

                if keyboard.is_pressed('='):
                    self.logger.log('Script Stopped.')
                    raise ExitMenuException
                    return

                if keyboard.is_pressed("["):
                    self.check_item()

                if keyboard.is_pressed("]"):
                    data = input("Insert Your targeted Monster : ")
                    self.targets = [int(dt) for dt in data.split(",")]
                    self.current_target = 0
                    print(self.targets)

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
