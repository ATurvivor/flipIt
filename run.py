#!/usr/bin/env python

from endGame import *
# globals and log imported from endGame
import numpy as np


def run(agents, environment=None):
    """
    Run game
    :param agents: list of agents
    :param environment: (optional) environment frame (example : mainWindow)
    :return:
    """
    # TODO check if variable environment is needed
    if globals.gDebug:
        print('Writing log in ' + str(globals.gLogFileName) + '\n')

    while not globals.gEndGame:
        if globals.gDebug:
            print('\nCurrent iteration : ' + str(globals.gIteration))
        log.writeLog(globals.gLogFileName, globals.gIteration, agents) # log data
        generateRandomSeeds(agents)
        endgame = decisionProcess(agents)
        if (endgame):
            verifyEndGame(agents)


def generateRandomSeeds(agents):
    """
    Generates random seeds for each agent
    :param agents: list of agents
    :return:
    """
    globals.gRandomSeeds = {agent.id:np.random.uniform(0,1.0) for agent in agents}

def decisionProcess(agents):
    """
    Flip for each agent
    :param agents: list of agents
    :return: boolean, whether game ends
    """
    flipped = {} #agents that flip or flip times for discrete/continuous respectively
    if globals.gGameType == 'Continuous':
        flipped=globals.gFlipped
        if(globals.gIteration==0.0):
            for agent in agents:#Initialize all agents flip times
                flipped[agent]=agent.flipDecision()[1]
        else:
            flipped[globals.gCurrentOwner] = globals.gCurrentOwner.flipDecision()[1] + globals.gIteration
            #Updates only previous owners flip time
            #This method doesn't yet work for continuous collisions

        globals.gFlipped=flipped
        globals.gIteration = np.minimum(np.amin(flipped.values()),globals.gGameEnd)
        flipval=globals.gIteration
        print(np.amin(flipped))
    elif globals.gGameType == 'Discrete':
        for agent in agents:
            flipped[agent]=agent.flipDecision()[0]
        globals.gIteration += 1
        flipval=True

    if globals.gDebug:
        print('Agents flip decisions : ' + str(flipped.values()))

    if(globals.gIteration>=globals.gGameEnd):
        return True

    if any(flipped.values()):
        # if one or more agents flipped, pick random
        flippedAgents = [agent for agent in flipped.keys() if flipped[agent]==flipval]
        updateScores(flippedAgents)
        updateCurrentOwner(flippedAgents)
    return False

def updateScores(agents):
    """
    Updates scores
    :param agents: list of agents
    :return:
    """
    globals.gCurrentOwner.updateScore()
    for agent in agents:
        agent.flipPenalty()
        agent.lastFlipTime = globals.gIteration
        agent.flip = False

def updateCurrentOwner(agents):
    """
    Updates current owner of resource
    :param agents: list of agents
    :return:
    """
    agent_order=np.random.permutation(agents)
    for agent in agent_order:
        agent.updateHistory()

    globals.gCurrentOwner = agent_order[-1]

