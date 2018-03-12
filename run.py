# -*- coding: utf-8 -*-

import sys
from os import getcwd
sys.path.append(getcwd())

from Tkinter import *
from ui.mainWindow import MainWindow


def launch():
    root = Tk()
    root.resizable(width=300, height=300)

    main_window = MainWindow(root)
    main_window.pack()

    root.mainloop()

if __name__ == '__main__':
    launch()