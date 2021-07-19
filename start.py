import os
import importlib
import pymem
import time

from core.exceptions import ExitMenuException

from update import run_update
from window.ui import MainMenu

os.system('cls')

try:
    import config
    if config.update_before_start:
        run_update()
except:
    run_update(force=True)

print_waiting_process = True
print_waiting_memory = True

inputData = None

def getProcess() :
    processes = pymem.process.list_processes()
    for value in processes:
        if value.szExeFile == b'SO3D.exe':
            return value

    return False


def get_memory_availability():
    baseAddr = int(0x400000) + int(0x010101CC)
    pointer = pymem.memory.read_int(pc, int(0x400000) + int(0x002E87A8))
    addr = pointer + int(0x5f0)
    return pymem.memory.read_int(pc, addr)


def load_module(inputData):
    from macro import cegel_farm, farming, auto_refine, potion

    importlib.reload(cegel_farm)
    importlib.reload(farming)
    importlib.reload(auto_refine)
    importlib.reload(potion)

    if inputData == "1":
        cegel_farm.CegelFarm().start()
    elif inputData == "2":
        farming.Farming().start()
    elif inputData == "3":
        auto_refine.AutoRefine().start()
    elif inputData == "4":
        potion.Potion().start()


def start_menu():
    print("MACRO READY!")
    print(
        "Menu: \n",
        "1. Cegel Farming\n",
        "2. General Farming\n",
        "3. Auto Refine\n",
        "4. Potion\n",
    )
    inputData = input("Answer ? ") or "0"

    try:
        load_module(inputData)
    except ExitMenuException as e:
        print("Exited...\n")
    except Exception as e:
        print("Something wrong. Exiting..")
        print(e)

    time.sleep(0.5)


while True:
    pm = pymem.Pymem()
    if getProcess():
        process = getProcess()
        pid = process.th32ProcessID
        pc = pymem.process.open(pid)
        try:
            get_memory_availability()
        except Exception as e:
            if print_waiting_memory:
                print("Loading..")
                # print(e)

                print_waiting_memory = False
        else:
            start_menu()
    else:
        if print_waiting_process:
            print('Waiting Process...')
            print_waiting_process = False
    
    time.sleep(0.2)
