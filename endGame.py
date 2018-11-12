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

def resetGame(agents):
    """
    Resets game
    :param agents : List of agents
    :param environment : (optional) mainwindow frame
    :return:
    """
    globals.gEndGame = True
    if globals.gDebug:
        print('Resetting game.')

    for ag in agents:
        ag.score = 0
        ag.flip = False
        ag.lastFlipTime = 0

    if globals.gDebug:
        print('END.')