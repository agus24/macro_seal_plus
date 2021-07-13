import sys
from datetime import datetime

from tkinter import *
from tkinter import scrolledtext

class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self, text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    def write(self, string):
        time = datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')
        self.text_area.insert(END, f"{string}")
        self.text_area.see(END)

    def flush(self):
        self.text_area.delete(1.0, END)

class Window:
    title = "Macro v2.0"
    text_area = None

    def __init__(self):
        self.window = Tk()
        self.window.title(self.title)

        self.window.geometry("600x600")

        self.frame = Frame(master=self.window)
        self.frame.pack_propagate(0) # Don't allow the widgets inside to determine the frame's width / height
        self.frame.pack(fill=BOTH, expand=1) #Expand the frame to fill the root window

        self.text_frame()
        sys.stdout = StdoutRedirector(self.text_area)

    def do_something(self):
        print("a")

    def text_frame(self):
        frame = Frame(self.window)
        self.text_area = scrolledtext.ScrolledText(frame, width=70, height=25)
        self.text_area.grid(column=0, row=100, sticky=S)
        self.text_area.config(background="white", foreground="black",
                    wrap='word')

        self.text_area.insert(END, "")
        frame.pack_propagate(0)
        frame.pack(fill=BOTH, expand=1)

    def kill(self):
        self.window.destroy()

    def add_button(self, label, command = None, width = 10, height=1, column=0, row=0):
        kwargs = {
            'master': self.frame,
            'text': label,
            'width': width,
            'height': height,
            'bg': "cyan"
        }

        if command:
            kwargs['command'] = command

        button = Button(**kwargs)
        button.grid(column=column, row=row, pady=(5, 5), padx=(10, 0), sticky=W+N+S)
        return button

    def loop(self):
        self.window.mainloop()
