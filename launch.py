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

def initGame():
    """

    :return:
    """
    setProperties(readProperties('config/test.properties'))

    if globals.gFiniteTime: # finite
        globals.gGameEnd = globals.gLastIteration
    else: # infinite
        if globals.gGameType == 0: # continuous
            globals.gGameEnd = np.random.exponential(scale=1.0 / globals.gEndGameProbability)
        elif globals.gGameType == 1: # discrete
            globals.gGameEnd = np.random.geometric(p=globals.gEndGameProbability)


def launch():
    initGame()

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
        globals.gLogFileName = 'logs/datalog_' + str(time.year) + str(time.month) + str(time.day) + '-' + \
                               str(time.hour) + 'h' + str(time.minute) + 'm' + str(time.second) + 's' + \
                               str(time.microsecond) + 'us.txt'

        if globals.gDebug:
            print('Writing log in ' + str(globals.gLogFileName) + '\n')

        run(agents)

if __name__ == '__main__':
    launch()