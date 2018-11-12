#!/usr/bin/env python

from config import log, globals


def endGame(agents):
    """
    Ends game
    :param agents: List of agents
    :return:
    """
    globals.gEndGame = True
    if globals.gDebug:
        print('\nGame ended.')
        for agent in agents:
            print('Agent ' + str(agent.id) + ' has a final score ' + str(agent.score))

def resetGame(agents):
    """
    Resets game
    :param agents : List of agents
    :param environment : (optional) mainwindow frame
    :return:
    """
    globals.gEndGame = True
    if globals.gDebug:
        print('\nResetting game.')

    for ag in agents:
        ag.score = 0
        ag.flip = False
        ag.lastFlipTime = 0

    if globals.gDebug:
        print('END.')