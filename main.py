#!/usr/bin/env python

import sys
from os import getcwd
sys.path.append(getcwd())

from tkinter import *
from ui.mainWindow import MainWindow

from simulations.run import *
from agents.agent import *
from config.properties import *


def main():
    """
    Run game
    :return:
    """
    setProperties(readProperties('config/parameters/test.properties'))
    #agent_params=[(1,.005),(1,.01),(2,(.005,.005)),(2,(.0025,.0025)),(0,.005),(0,.01)]

    if globals.gEnvironment:
        root = Tk()
        root.resizable(width=300, height=300)

        agents = [Agent(strategy=0, strategyParam=0.01, type='LM'), Agent(strategy=-1)]
        globals.gCurrentOwner = agents[0]  # default
        main_window = MainWindow(root, agents)
        main_window.pack()

        root.mainloop()

    else:
        agents = [Agent(strategy=0), Agent(strategy=0)]
        print(run(agents))

if __name__ == '__main__':
    main()