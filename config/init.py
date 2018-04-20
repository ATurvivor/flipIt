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

    if environment:
        if environment.timeFrame.time.get() == 1: # finite
            globals.gGameEnd = globals.gLastIteration
        elif globals.gGameType == 0: # infinite and continuous
            globals.gGameEnd = np.random.exponential(scale=1.0 / float(environment.timeFrame.probability.get()))
        else: # infinite and discrete
            globals.gGameEnd = np.random.geometric(p=float(environment.timeFrame.probability.get()))
    else:
        if globals.gFiniteTime == 1: # finite
            globals.gGameEnd = globals.gLastIteration
        elif globals.gGameType == 0: # infinite and continuous
            globals.gGameEnd = np.random.exponential(scale=1.0 / globals.gEndGameProbability)
        else: # infinite and discrete
            globals.gGameEnd = np.random.geometric(p=globals.gEndGameProbability)