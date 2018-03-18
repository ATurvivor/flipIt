#!/usr/bin/env python

import globals


def logHeader(fileName):
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

    # TODO : complete log
    log = str(it) + ',' + str(agents[0].score) + ',' + str(agents[1].score)
    f.write(log + '\n')

    if globals.gDebug:
        print('Log : ' + log)

    f.close()

if __name__ == '__main__':
    writeLog()