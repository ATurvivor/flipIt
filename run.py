from ext import globals, log
from datetime import datetime
from time import sleep

def run(fileName, agents, environment=None):
    """
    Run game
    :param agents: List of agents
    :param environment: (optional) environment frame (example : mainWindow)
    :return:
    """
    globals.gIteration = 0

    print(fileName)
    #while not globals.gEndGame:
    if not globals.gEndGame:
        # at each iteration
        #if environment:
        #    environment.upperFrame.displayRun()

        log.log(fileName, globals.gIteration, agents) # log data
        # calculateRandomSeeds()
        # decisionProcess()
        # update()
        # verifyEndGame()

        globals.gIteration += 1
        print(globals.gIteration)

    sleep(10)
    run(agents, environment)