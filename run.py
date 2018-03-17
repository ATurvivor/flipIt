from ext import globals, log

def run(fileName, agents, environment=None):
    """
    Run game
    :param agents: List of agents
    :param environment: (optional) environment frame (example : mainWindow)
    :return:
    """
    globals.gIteration = 0

    print(fileName)
    while not globals.gEndGame:
        log.writeLog(fileName, globals.gIteration, agents) # log data
        # calculateRandomSeeds()
        # decisionProcess()
        # updateScores()
        # verifyEndGame()

        globals.gIteration += 1
        print(globals.gIteration)

def calculateRandomSeeds():
    nbAgents = globals.gNbAgents
