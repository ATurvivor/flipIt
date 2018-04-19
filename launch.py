#!/usr/bin/env python

import sys
from os import getcwd
sys.path.append(getcwd())

from Tkinter import *
from ui.mainWindow import MainWindow

from run import *
from agents.agent import *
from config.properties import *

def launch():
    """
    Run game
    :return:
    """
    setProperties(readProperties('config/test.properties'))

    agents = [Agent() for _ in range(globals.gNbAgents)]
    globals.gCurrentOwner = agents[0]  # default

    if globals.gEnvironment:
        root = Tk()
        root.resizable(width=300, height=300)

        main_window = MainWindow(root, agents)
        main_window.pack()

        root.mainloop()

    else:
        run(agents)

if __name__ == '__main__':
    launch()