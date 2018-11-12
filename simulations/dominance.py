from run import initParameters, decisionProcess, generateRandomSeeds
from endGame import *
from config.properties import readProperties, setProperties
from config.log import writeLog
from agents.agent import *

def run_dominance_sim(agents):
    """
    Run game
    :param agents: list of agents
    :param environment: (optional) environment frame (example : mainWindow)
    :return:
    """
    initParameters() # initialise game parameters

    if globals.gDebug:
        print('Writing log in ' + str(globals.gLogFileName) + '\n')

    while not globals.gEndGame:
        if globals.gDebug:
            print('\nCurrent iteration : ' + str(globals.gIteration))

        generateRandomSeeds(agents)

        if decisionProcess(agents):
            # Last iteration
            writeLog(globals.gLogFileName, globals.gIteration, agents) # log data
            endGame(agents)
            resetGame(agents)

if __name__ == '__main__':
    setProperties(readProperties('config/test.properties'))
    agent_params=[(1,.005),(1,.01),(2,(.005,.005)),(2,(.0025,.0025)),(0,.005),(0,.01)]

    agents = [Agent(strategy=1, strategyParam=.005), Agent(strategy=1, strategyParam=.005)]

    agents = [Agent(strategy=agent_params[idx][0], strategyParam=agent_params[idx][1]) for idx in
                      range(globals.gNbAgents)]
    globals.gCurrentOwner = agents[0]

    run_dominance_sim(agents)

    print(agents[0].score, agents[1].score)