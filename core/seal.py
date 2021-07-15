import ctypes
import re
import win32process
import win32api
import pyautogui
import pymem
import sys
import time
import threading
import struct

pm = pymem.Pymem("SO3D.exe")

baseAddressMouse = int(0x400000) + int(0x00D8C4F4)
pointerMouse = pm.read_int(baseAddressMouse)

baseAddressStat = int(0x400000) + int(0x002E87A8)
pointerStat = pm.read_int(baseAddressStat)

mouseX = (pointerMouse) + int(0x2c0)
mouseY = (pointerMouse) + int(0x2c4)


def moveMouse(x, y):
    pyautogui.moveTo(x, y)
    # pm.write_short(mouseX, x)
    # pm.write_short(mouseY, y)


def getPosition():
    # print("(x, y)")
    # print(f"({pm.read_short(mouseX)}, {pm.read_short(mouseY)})")
    print(pyautogui.position())


def getStatList():
    mpw = (pointerStat) + int(0x450)
    defend = (pointerStat) + int(0x454)
    mspd = (pointerStat) + int(0x468)
    hp = (pointerStat) + int(0x46c)

    print("mpw : " + str(pm.read_short(mpw)))
    print("defend : " + str(pm.read_short(defend)))
    print("mspd : " + str(pm.read_short(mspd)))
    print("hp : " + str(pm.read_short(hp)))


def makeStatHp(value):
    print("hp : "+value)


def forcePid(identifier):
    pid = identifier


def getItemQty():
    slot_1 = (pointerStat) + 1520
    slot_2 = (pointerStat) + 1520 + 116
    slot_3 = (pointerStat) + 1520 + 116 + 116
    slot_4 = (pointerStat) + 1520 + 116 + 116 + 116
    slot_5 = (pointerStat) + 1520 + 116 + 116 + 116 + 116

    sys.stdout.write(
        "slot : " + str(pm.read_short(slot_1)) +
        "  slot : " + str(pm.read_short(slot_2)) +
        "  slot : " + str(pm.read_short(slot_3)) +
        "  slot : " + str(pm.read_short(slot_4)) +
        "  slot : " + str(pm.read_short(slot_5)) + "\r"
    )
    sys.stdout.flush()
    # print("slot : 300")


def getPid():
    return pid


def setPid(id):
    pid = pid
    pc = pymem.process.open(pid)


def getItemValue():
    item = []
    baseAddressStat = pm.read_int(int(0x400000) + int(0x002E87A8))

    for i in range(0, 40):
        calc = (pointerStat) + 1520 + (116 * i)
        item.append({
            "slot": i,
            "address": calc,
            "qty": pm.read_short(calc),
            "plus": pm.read_short(calc - 8),
            "item_id": pm.read_short(calc - 12)
        })
    return item


def getUserId():
    baseAddr = int(0x400000) + int(0x002E9A24)
    pointer = pm.read_int(baseAddr)
    idAddress = pointer + int(0x1678)
    return  pm.read_string(idAddress, 16)


def spamSkill():
    baseAddr = int(0x400000) + int(0x003DB34C)
    pointer = pm.read_int(baseAddr)
    spamAddr = pointer + int(0x1D00)
    val = pm.write_int(spamAddr, 3)


def getItemStatus():
    mpw = (pointerStat) + int(0x450)
    defend = (pointerStat) + int(0x454)
    mspd = (pointerStat) + int(0x468)
    hp = (pointerStat) + int(0x46c)
    dmg = (pointerStat) + int(0x44c)

    status = {
        "mpw": pm.read_short(mpw),
        "defend": pm.read_short(defend),
        "mspd": pm.read_short(mspd),
        "hp": pm.read_short(hp),
        "dmg": pm.read_short(dmg),
    }
    return status


def setTarget(target):
    baseAddr = int(0x400000) + int(0x002E9A24)
    pointer = pm.read_int(baseAddr)
    addr = pointer + int(0x1670)
    pm.write_int(addr, target)
    pm.write_int(int(0x400000) + int(0x00D9AEF8), target)


def getCurrentTarget():
    baseAddr = int(0x400000) + int(0x002E9A24)
    pointer = pm.read_int(baseAddr)
    addr = pointer + int(0x1670)
    return pm.read_int(addr)

def getCurrentTargetArrow():
    baseAddr = int(0x400000) + int(0x00D9AEF8)
    return pm.read_int(baseAddr)


def get_dialog():
    baseAddr = int(0x400000) + int(0x002D3DF4)
    return pm.read_int(baseAddr)


def set_dialog(value):
    baseAddr = int(0x400000) + int(0x002D3DF4)
    pm.write_int(baseAddr, value)


def get_item_bank_status():
    baseAddr = int(0x400000) + int(0x00D613D0)
    return pm.read_int(baseAddr)

def get_atb_status():
    baseAddr = int(0x400000) + int(0x002E46A8)
    pointer = pm.read_int(baseAddr)
    addr = pointer + int(0x158)
    return pm.read_int(addr)


def get_pointer_data(address, offset):
    baseAddr = int(0x400000) + int(address)
    pointer = pm.read_int(baseAddr)
    print("pointer : " + hex(pointer))
    addr = pointer + int(offset)
    print("address :" + hex(addr))
    return pm.read_int(addr)
