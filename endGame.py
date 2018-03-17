import numpy as np

from ext import globals, log

def verifyEndGame():
    """
    Verifies if we reached end of game
    :return:
    """
    if (np.random.uniform(0,1) < globals.gEndGameProbability):
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
    log.log(globals.gLogFileName, globals.gIteration, agents)

    globals.gEndGame = True

    for ag in agents:
        ag.score = 0

    if environment:
        environment.resetMainWindow()