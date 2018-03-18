#!/usr/bin/env python

import sys
from os import getcwd
sys.path.append(getcwd())

# environment
from Tkinter import *
from ui.mainWindow import MainWindow

from run import *
from agents.agent import *
from config.properties import *
from datetime import datetime


def launch():
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
        # data log file name
        time = datetime.now()
        globals.gLogFileName = 'logs/datalog_' + str(time.year) + str(time.month) + str(time.day) + '-' +\
                               str(time.hour) + 'h' + str(time.minute) + 'm' + str(time.second) + 's' +\
                               str(time.microsecond) + 'us.txt'
        run(agents)

if __name__ == '__main__':
    launch()