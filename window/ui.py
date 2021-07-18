import os
import pymem
import time
import subprocess

import pymem
import tkinter as tk

from core.exceptions import ExitMenuException

from .window import Window


class MainMenu(Window):
    print_waiting_process = True
    print_waiting_memory = True
    start = False
    pc = None
    macro_ready = False
    is_macro_choosen = False

    def print_something(self):
        print('test')

    def cegel_farm(self):
        if not self.macro_ready:
            print("Macro not ready")
            return

        from macro.cegel_farm import CegelFarm
        cegel_farm = CegelFarm()
        cegel_farm.print_hotkey()
        self.is_macro_choosen = True

        while True:
            try:
                cegel_farm.start()
            except ExitMenuException as e:
                self.is_macro_choosen = False
                break
            except Exception as e:
                print(e)
                break

            time.sleep(0.2)

    def get_memory_availability(self):
        baseAddr = int(0x400000) + int(0x010101CC)
        pointer = pymem.memory.read_int(self.pc, int(0x400000) + int(0x002E87A8))
        addr = pointer + int(0x5f0)
        return pymem.memory.read_int(self.pc, addr)

    def get_process(self):
        processes = pymem.process.list_processes()
        for value in processes:
            if value.szExeFile == b'SO3D.exe':
                return value

        return False
    
    def prepare(self):
        self.force_stop()
        subprocess.run([".\\bin\\start.bat"])

    def pause(self):
        print("Pausing")
        self.start = False
        self.print_waiting_process = True
        self.print_waiting_memory = True

    def start(self):
        try:
            self.add_button("Start", command=self.prepare, row=0)
            self.add_button("Exit", command=self.kill, row=2)
        except ExitMenuException as e:
            print("Exited...")
        except Exception as e:
            if self.macro_ready:
                print("Something wrong. Exiting..")
                print(e)
            else:
                print("Macro not ready")

        self.loop()
