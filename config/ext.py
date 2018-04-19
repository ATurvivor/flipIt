#!/usr/bin/env python

from datetime import datetime
from config import globals
import numpy as np


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

# TODO : complete log

def writeLogHeader(fileName):
    """
    Log file header
    :param fileName:
    :return:
    """
    return 0


def writeLog(fileName, it, agents):
    """
    Logs data
    :param agents: List of agents
    :return:
    """

    f = open(fileName, 'a')

    log = str(it) + ',' + str(agents[0].score) + ',' + str(agents[1].score)
    f.write(log + '\n')

    if globals.gDebug:
        print('Log : ' + log)

    f.close()

if __name__ == '__main__':
    writeLog()