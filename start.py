import os
import pymem
import time

from core.exceptions import ExitMenuException

from window.ui import MainMenu

from update import run_update

os.system('cls')

try:
    import config
    if config.update_before_start:
        run_update()
except:
    run_update()

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

def start_menu():
    print("MACRO READY!")
    print(
        "Menu: \n",
        "1. cegel\n",
        "2. ant nest\n",
        "3. auto tempa\n",
        "0. ts\n"
    )
    inputData = input("Answer ? ") or "0"

    try:
        if inputData == "1":
            from macro.cegel_farm import CegelFarm
            CegelFarm().start()
        elif inputData == "2":
            import macro.ant_farm
        elif inputData == "3":
            import macro.auto_refine
    except ExitMenuException as e:
        print("Exited...")
    except Exception as e:
        print("Something wrong. Exiting..")
        print(e)

    time.sleep(0.5)

# MainMenu().start()
while True:
    pm = pymem.Pymem()
    if getProcess() :
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
