#!/usr/bin/env python

from datetime import datetime
import numpy as np
import globals

def initLogFileName():
    """
    Initialise log file name
    :return:
    """
    time = datetime.now()
    fname = 'logs/datalog_' + str(time.year) + str(time.month) + str(time.day) + '-' + \
            str(time.hour) + 'h' + str(time.minute) + 'm' + str(time.second) + 's' + \
            str(time.microsecond) + 'us.txt'
    return fname


def initGame(environment=None):
    """
    Initialises game parameters
    :param environment:
    :return:
    """
    globals.gLogFileName = initLogFileName() # initialise log file name
    if (environment and environment.timeFrame.time.get() == 1) or globals.gFiniteTime == 1: # finite
        globals.gGameEnd = globals.gLastIteration

    elif (environment and environment.timeFrame.time.get() == 0) or globals.gFiniteTime == 0: # infinite
        if globals.gGameType == 0: # continuous
            globals.gGameEnd = np.random.exponential(scale=1.0 / globals.gEndGameProbability)
        elif globals.gGameType == 1: # discrete
            globals.gGameEnd = np.random.geometric(p=globals.gEndGameProbability)
