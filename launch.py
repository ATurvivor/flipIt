# -*- coding: utf-8 -*-

import sys
from os import getcwd
sys.path.append(getcwd())

from Tkinter import *
from ui.mainWindow import MainWindow

from agents.agent import *
from config.properties import *

from run import *

def launch():
    setProperties(readProperties('config/test.properties'))

    agents = [Agent(strategy=0), Agent(strategy=0)] # 0 : random

    if globals.gEnvironment:
        root = Tk()
        root.resizable(width=300, height=300)

        main_window = MainWindow(root, agents)
        main_window.pack()

        root.mainloop()

    else:
        run()

if __name__ == '__main__':
    launch()