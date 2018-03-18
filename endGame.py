#!/usr/bin/env python

import numpy as np
from ext import globals, log

def verifyEndGame(agents):
    """
    Verifies if we reached end of game
    :param agents: List of agents
    :return:
    """
    if (np.random.uniform(0,1) < globals.gEndGameProbability):
        globals.gEndGame = True
        if globals.gDebug:
            print('\nGame ended.')
        log.writeLog(globals.gLogFileName, globals.gIteration, agents)
        resetGame(agents)

def resetGame(agents, environment=None):
    """
    Resets game
    :param agents : List of agents
    :param environment : (optional) mainwindow frame
    :return:
    """
    if globals.gDebug:
        print('Resetting game.')

    for ag in agents:
        ag.score = 0
        ag.flip = False
        ag.lastFlipTime = 0

    if environment:
        environment.resetMainWindow()

    if globals.gDebug:
        print('END.')