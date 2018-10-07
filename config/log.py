#!/usr/bin/env python
from config import globals
from datetime import datetime

# TODO : complete log

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

    agentsLog = ""
    for ag in agents:
        agentsLog += ',' + str(ag.score)
    log = str(it) + agentsLog
    f.write(log + '\n')

    if globals.gDebug:
        print('Log : ' + log)

    f.close()

if __name__ == '__main__':
    writeLog()