import keyboard
import pywinauto as p

from time import sleep
from datetime import datetime

from core import auto_purchase
from core import discord
from core import macro
from core import seal

from core.constants import *
from core.logger import Logger


class AutoRefine:
    def __init__(self):
        print("auto_refine.py")
        self.user_id = seal.getUserId()
        self.keyboard = p.keyboard
        self.last_atb_slot = 1
        self.force_stop = False

        # SETTINGS
        self.atb_purchase_qty = config.atb_purchase_qty
        self.atb_per_purchase = config.atb_per_purchase
        self.wrs_brs_diamond_per_purchase = config.wrs_brs_diamond_per_purchase
        self.pd_grs_per_purchase = config.pd_grs_per_purchase
        self.max_tempa = config.max_tempa

        self.logger = Logger(user_id, file_name="_refine_log_")

    def get_inventory(self):
        return seal.getItemValue()

    def run_refine(self):
        inventory = self.get_inventory()
        plus = inventory[0]['plus']

        self.logger.log(f"current atb position : {self.last_atb_slot}")

        print(f"current atb position : {self.last_atb_slot}")
        if inventory[0]['item_id'] == 0:
            print("ITEM PECAH!!")
            time = datetime.now().strftime("%Y-%m-%d %H:%M")
            text = f"@everyone \n**ITEM PECAH!!** \nid : {user_id}\nIgn: \ntgl jam : {time}\n item: \nkronologi: lupa atb"
            discord.send_message(text)
            self.force_stop = True
            self.logger.log("ITEM PECAH!!")
            return

        if self.last_atb_slot == 0:
            print("purchasing ATB")
            self.logger.log("Purchasing ATB")
            self.purchase_item(auto_purchase.ITEM['atb'], self.atb_purchase_qty)
            sleep(1.5)
            self.get_atb_from_bank()
            self.last_atb_slot = 1

        if plus < 9 and plus > 6:
            print(f"refining to {plus+1}")
            self.logger.log(f"Refining to {plus+1}")
            self.refine_7_to_9(inventory)

        elif plus >= 9 and plus < self.max_tempa:
            print(f"refining to {plus+1}")
            self.logger.log(f"Refining to {plus+1}")
            self.refine_9_to_12(inventory)

        elif plus == 12:
            print("SUKSES +12 BOI")
            self.logger.log("SUKSES +12 BOI!!")
            discord.send_message(f"@everyone SUKSES JADI +12 BOII di id : {user_id}")

        if plus + 1 == self.get_item_result():
            print("SUKSES TEMPA")
            self.logger.log("SUKSES TEMPA")

        if self.max_tempa == self.get_item_result():
            discord.send_message(f"@everyone SUKSES TEMPA JADI {self.max_tempa} di id : {user_id}")
            self.logger.log(f"SUKSES TEMPA KE +{self.max_tempa}")
            self.force_stop = True

        if plus == 11:
            self.logger.log("Item Sukses jadi +11")
            discord.send_message(f"Item sukses jadi +11 di id : {user_id}")

    def refine_7_to_9(self, inventory):
        diamond = self.find_item_position(DIAMOND)
        wrs = self.find_item_position(WRS)
        brs = self.find_item_position(BRS)
        qty = 0

        if not wrs:
            print("purchasing wrs")
            self.purchase_item(auto_purchase.ITEM['wrs'], self.wrs_brs_diamond_per_purchase)
            qty = qty + self.wrs_brs_diamond_per_purchase
            sleep(0.5)

        if not brs:
            print("purchasing brs")
            self.purchase_item(auto_purchase.ITEM['brs'], self.wrs_brs_diamond_per_purchase)
            qty = qty + self.wrs_brs_diamond_per_purchase
            sleep(0.5)

        if not diamond:
            print("purchasing diamond")
            self.purchase_item(auto_purchase.ITEM['diamond'], self.wrs_brs_diamond_per_purchase)
            qty = qty + self.wrs_brs_diamond_per_purchase
            sleep(0.5)

        if not wrs or not brs or not diamond:
            print("getting item from bank")
            self.get_item_from_bank(qty)
            return

        if self.force_stop:
            print("self.force_stop triggered")
            self.force_stop = True
            return

        self.open_refine()

        self.move_item(REFINE_INVENTORY[0], REFINE_ITEM)
        self.move_item(REFINE_INVENTORY[diamond], REFINE_GEM)
        self.move_item(REFINE_INVENTORY[brs], REFINE_BRS)
        self.move_item(REFINE_INVENTORY[wrs], REFINE_WRS)
        self.move_atb()

        seal.moveMouse(*REFINE_OK)
        sleep(0.5)
        macro.mouseClick()

        seal.moveMouse(*REFINE_OK_CONFIRM)
        sleep(0.5)
        macro.mouseClick()
        sleep(8)

    def refine_9_to_12(self, inventory):
        pd = self.find_item_position(PD)
        grs = self.find_item_position(GRS)
        qty = 0

        if not pd:
            print("purchasing pd")
            self.purchase_item(auto_purchase.ITEM['pd'], self.pd_grs_per_purchase)
            qty = qty + self.pd_grs_per_purchase
            sleep(0.5)

        if not grs:
            print("purchasing grs")
            self.purchase_item(auto_purchase.ITEM['grs'], self.pd_grs_per_purchase)
            qty = qty + self.pd_grs_per_purchase
            sleep(0.5)

        if not pd or not grs:
            print("getting item from bank")
            self.get_item_from_bank(qty)
            sleep(0.5)
            return

        if self.force_stop:
            print("self.force_stop triggered")
            self.force_stop = True
            return

        self.open_refine()

        self.move_item(REFINE_INVENTORY[0], REFINE_ITEM)
        self.move_item(REFINE_INVENTORY[pd], REFINE_GEM)
        self.move_item(REFINE_INVENTORY[grs], REFINE_GRS)
        self.move_atb()

        seal.moveMouse(*REFINE_OK)
        sleep(0.5)
        macro.mouseClick()

        seal.moveMouse(*REFINE_OK_CONFIRM)
        sleep(0.5)
        macro.mouseClick()
        sleep(8)

    def open_refine(self):
        print(seal.get_dialog() == DIALOG['refine'])
        print(seal.get_dialog() == DIALOG['transaction'])
        print(seal.get_dialog())
        while seal.get_dialog() == 0:
            seal.moveMouse(383, 301)
            sleep(0.2)
            macro.mouseClick()

        while seal.get_dialog() == DIALOG['transaction']:
            macro.mouseClick()

    def find_item_position(self, item_id):
        inventory = self.get_inventory()
        for inven in inventory:
            if inven['item_id'] == item_id:
                return inven['slot']

    def get_item_from_bank(self, qty):
        while seal.get_dialog() == 0:
            seal.moveMouse(529, 464)
            sleep(0.5)
            macro.mouseClick()
            sleep(0.5)
            seal.moveMouse(*REFINE_OK_CONFIRM)
            sleep(0.5)
            macro.mouseClick()
            sleep(1)
        self.keyboard.send_keys('{1 down}' '{1 up}')
        self.keyboard.send_keys('{1 down}' '{1 up}')
        self.keyboard.send_keys('{1 down}' '{1 up}')
        self.keyboard.send_keys('{1 down}' '{1 up}')
        self.keyboard.send_keys('{ENTER}')
        sleep(0.5)
        for i in range(0, qty + 2):
            if not self.has_empty_slot():
                print("inven penuh batal tarik barang")
                break
            seal.moveMouse(BANK_POSITION[i][0], BANK_POSITION[i][1])
            macro.mouseDown()
            seal.moveMouse(411, 214)
            macro.mouseUp()
            sleep(0.2)
            self.keyboard.send_keys('{ENTER}')
            sleep(0.2)

        while seal.get_dialog() == DIALOG['bank']:
            self.keyboard.send_keys("{VK_ESCAPE}")
            sleep(0.5)
            seal.moveMouse(328, 118)
            sleep(0.5)
            macro.mouseClick()

    def move_item(self, position1, position2):
        seal.moveMouse(position1[0], position1[1])
        sleep(0.2)
        macro.mouseDown()
        seal.moveMouse(position2[0], position2[1])
        sleep(0.2)
        macro.mouseUp()
        sleep(0.2)

    def move_atb(self):
        self.move_item(ITEM_CASH[self.last_atb_slot], REFINE_ATB)
        self.last_atb_slot = self.last_atb_slot + 1
        if self.last_atb_slot > self.atb_per_purchase:
            self.last_atb_slot = 0

    def get_item_result(self):
        return self.get_inventory()[0]['plus']

    def has_empty_slot(self):
        inventory = self.get_inventory()

        for inven in inventory:
            if inven['item_id'] == 0:
                return True

    def get_atb_from_bank(self):
        self.keyboard.send_keys(
            "{VK_LMENU down}"
            "{v down}"
            "{v up}"
            "{VK_LMENU up}"
        )
        sleep(0.3)
        seal.moveMouse(*REFINE_OK_CONFIRM)
        sleep(0.5)
        macro.mouseClick()
        sleep(0.5)
        for i in range(0, self.atb_per_purchase + 5):
            seal.moveMouse(ITEM_BANK[i][0], ITEM_BANK[i][1])
            macro.mouseDown()
            seal.moveMouse(433, 194)
            macro.mouseUp()
            sleep(0.2)
            seal.moveMouse(*REFINE_OK_CONFIRM)
            sleep(0.5)
            macro.mouseClick()

        sleep(0.5)
        while seal.get_item_bank_status() == 1:
            seal.moveMouse(337, 105)
            sleep(0.5)
            macro.mouseClick()

        sleep(1)
        self.keyboard.send_keys(
            "{VK_LMENU down}"
            "{a down}"
            "{a up}"
            "{VK_LMENU up}"
        )
        sleep(0.5)

    def purchase_item(self, item_id, qty):
        retry_limit = 3
        for i in range(0, retry_limit):
            status, purchase_limit, purchased_qty = auto_purchase.purchase(item_id, qty)
            if not status:
                if purchase_limit:
                    self.force_stop = True
                    discord.send_message(f"**Purchase Limit Reached** for id : {user_id}")
                    return

                qty = qty - purchased_qty

                print("purchase failed")
                print(f"retrying to purchase {purchased_qty} more item")
                self.logger.log("Purchase Failed")
                self.logger.log(f"retrying to purchase {purchased_qty} more item")

            return

        print("Cannot purchase : something went wrong")
        self.logger.log("Cannot purchase : something went wrong")
        message = f"Failed Purchase : something went wrong. ID : {user_id} purchased: {purchased_qty}, remaining: qty"
        discord.send_message(message)

    def print_hotkey(self):
        help_text = [
            "HOTKEYS: ",
            "[-] start refine",
            "[c] force stop (tahan tombolnya aja sampe berenti)",
            "[/] set atb position (pake kalo atbnya error aja)",
            "[=] print mouse position"
        ]
        
        print("\n")
        print("\n".join(help_text))

    def print_settings(self):
        settings = [
            "SETTINGS : ",
            f"self.atb_purchase_qty: {self.atb_purchase_qty}",
            f"self.atb_per_purchase: {self.atb_per_purchase}",
            f"self.wrs_brs_diamond_per_purchase: {self.wrs_brs_diamond_per_purchase}",
            f"self.pd_grs_per_purchase: {self.pd_grs_per_purchase}",
            f"self.max_tempa: {self.max_tempa}",
            "\n\nFOR PURCHASE: ",
            f"username: {auto_purchase.username}",
            f"password: {auto_purchase.password}",
            f"password_bank: {auto_purchase.password_bank}",
        ]
        print("\n")
        print("\n".join(settings))

    def start(self):
        self.print_settings()
        self.print_hotkey()

        while True:
            if keyboard.is_pressed('ctrl'):
                if keyboard.is_pressed('-'):
                    sleep(0.5)
                    print("Starting.. Hold C to stop.")
                    while True:
                        self.run_refine()
                        if self.force_stop:
                            self.force_stop = False
                            break

                        if keyboard.is_pressed('c'):
                            print("stopping")
                            break

            if keyboard.is_pressed("="):
                print(seal.getPosition())
                print(seal.getItemValue())
                sleep(0.5)

            if keyboard.is_pressed("/"):
                self.last_atb_slot = int(input("atb_slot : ") or 1)
                sleep(0.5)
