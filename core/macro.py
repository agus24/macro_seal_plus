import pyautogui
from core import seal
from time import sleep
import pywinauto as p
from core.constants import DIALOG, REFINE_OK_CONFIRM, BANK_INVENTORY

k = p.keyboard
delay = 0.5

slot = [
    [309, 134],
    [331, 134],
    [361, 134],
    [391, 134],
    [421, 134],
    [451, 134],
    [481, 134],
    [511, 134],
    # [301, 123],
    # [331, 123],
    # [361, 123],
    # [391, 123],
    # [421, 123],
    # [451, 123],
    # [481, 123],
    # [511, 123],
]

shop = [555, 227]

def mouseClick() :
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    sleep(delay)

def mouseDown() :
    pyautogui.mouseDown()
    sleep(delay)

def mouseUp() :
    pyautogui.mouseUp()
    sleep(delay)

def moveMouse(x, y):
    pyautogui.moveTo(x, y)

def sell(x, y) :
    seal.moveMouse(x, y)
    sleep(delay)
    mouseDown()
    seal.moveMouse(122, 219)
    mouseUp()
    seal.moveMouse(434, 323)
    mouseClick()
    seal.moveMouse(389, 391)
    mouseClick()
    seal.moveMouse(451, 337)
    mouseClick()
    sleep(delay * 2)


def sellSlot1():
    sell(308, 143)


def sellSlot2():
    sell(348, 143)


def sellSlot3():
    sell(377, 143)


def sellSlot4():
    sell(409, 143)


def sellSlot5():
    sell(441, 143)


def open_bank():
    seal.moveMouse(563, 461)
    sleep(delay)

    mouseClick()
    sleep(delay)

    seal.moveMouse(*REFINE_OK_CONFIRM)
    sleep(delay)

    mouseClick()
    sleep(delay)

    k.send_keys( '{1 down}' '{1 up}' )
    k.send_keys( '{1 down}' '{1 up}' )
    k.send_keys( '{1 down}' '{1 up}' )
    k.send_keys( '{1 down}' '{1 up}' )
    sleep(delay)

    k.send_keys('{ENTER}')
    sleep(delay)


def close_bank():
    seal.moveMouse(477, 563)
    mouseClick()

    p.keyboard.send_keys("{VK_ESCAPE}")

    seal.moveMouse(329, 120)
    mouseClick()


def move_to_bank(slot):
    seal.moveMouse(*BANK_INVENTORY[slot])
    sleep(delay)

    mouseDown()
    sleep(delay)

    seal.moveMouse(197, 272)
    sleep(delay)

    mouseUp()
    seal.moveMouse(449, 319)
    sleep(delay)

    mouseClick()
    seal.moveMouse(391, 392)
    sleep(delay)

    mouseClick()
    k.send_keys('{ENTER}')
    sleep(delay)


def sellTrashItem() :
    openShop()
    for idx, (x, y) in enumerate(slot) :
        if idx == 0 :
            continue
        else :
            sell(x, y)
    print("Done Selling Trash Item.")

def openShop() :
    if not checkShop() :
        print("Shop is closed.")
        seal.moveMouse(shop[0], shop[1])
        sleep(1)
        mouseClick()
        k.send_keys("{ENTER}")
        sleep(delay)

def buyPot() :
    openShop()
    buyItem(62, 355)
    buyItem(62, 391)
    p.keyboard.send_keys("{VK_ESCAPE}")

def buyItem(x, y) :
    seal.moveMouse(x, y)
    sleep(delay)
    mouseDown()
    sleep(delay)
    seal.moveMouse(slot[0][0], slot[0][1])
    sleep(delay)
    mouseUp()
    seal.moveMouse(444, 320)
    mouseClick()
    seal.moveMouse(386, 397)
    mouseClick()
    seal.moveMouse(450, 340)
    mouseClick()
    sleep(delay)

def closeBSIfOpen() :
    sleep(0.1)
    print('check if bank or shop is open')
    if checkShop() :
        k.send_keys("{VK_ESCAPE}")
    if checkBank() :
        k.send_keys("{VK_ESCAPE}")

def checkBank():
    return seal.get_dialog() == DIALOG['bank']

def checkShop():
    return seal.get_dialog() == DIALOG['shop']

def checkItemBank():
    return seal.get_item_bank_status() == 1
