import numpy as np

from ext.globals import *
from ext.log import *

def verifyEndGame():
    """
    Verifies if we reached end of game
    :return:
    """
    if (np.random.uniform(0,1) < gEndGameProbability):
        gEndGame = True
        #update()
        #log()
        resetGame()


def resetGame(agents, environment=None):
    """
    Resets game
    :param agents : List of agents
    :param environment : (optional) mainwindow frame
    :return:
    """
    log(gLogFileName, gIteration, agents)

    for ag in agents:
        ag.score = 0

    if environment:
        environment.resetMainWindow()