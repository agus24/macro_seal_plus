import pyautogui
from core import seal
from time import sleep
import pywinauto as p
from core.constants import DIALOG

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

def itemToBank():
    seal.moveMouse(790, 228)
    sleep(delay)
    mouseClick()
    sleep(delay)
    k.send_keys('{ENTER}')
    sleep(delay)
    k.send_keys( '{r down}' '{r up}' )
    k.send_keys( '{a down}' '{a up}' )
    k.send_keys( '{h down}' '{h up}' )
    k.send_keys( '{a down}' '{a up}' )
    k.send_keys( '{s down}' '{s up}' )
    k.send_keys( '{i down}' '{i up}' )
    k.send_keys( '{a down}' '{a up}' )
    sleep(delay)
    k.send_keys('{ENTER}')
    seal.moveMouse(334, 119)
    sleep(delay)
    mouseDown()
    sleep(delay)
    seal.moveMouse(117, 227)
    sleep(delay)
    mouseUp()
    seal.moveMouse(419, 319)
    mouseClick()
    mouseClick()
    mouseClick()
    k.send_keys('{ENTER}')
    seal.moveMouse(416, 451)
    mouseClick()
    seal.moveMouse(499, 299)
    mouseClick()
    closeBSIfOpen()

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
    return seal.get_freeze_dialog() == DIALOG['bank']

def checkShop():
    return seal.get_freeze_dialog() == DIALOG['shop']

def checkItemBank():
    return seal.get_item_bank_status() == 1
