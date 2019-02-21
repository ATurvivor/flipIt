#!/usr/bin/env python

from endGame import *
from config.log import initLogFileName, writeLog

import numpy as np


def initParameters(agents):
    """
    Initialises game parameters
    :param environment:
    :return:
    """
    globals.gLogFileName = initLogFileName() # initialise log file name
    globals.gAgentStartId = 0
    globals.gEndGame = False
    globals.gCurrentOwner = agents[globals.gCurrentOwnerId]

    if globals.gFiniteTime: # finite
        globals.gLastIteration = globals.gGameLength
    elif globals.gContinuous: # infinite and continuous
        globals.gLastIteration = np.random.exponential(scale=1.0 / globals.gEndGameProbability)
    else: # infinite and discrete
        globals.gLastIteration = np.random.geometric(p=globals.gEndGameProbability)

def generateRandomSeeds(agents):
    """
    Generates random seeds for each agent
    :param agents: list of agents
    :return:
    """
    globals.gRandomSeeds = {agent.id:np.random.uniform(0, 1.0) for agent in agents}

def run(agents):
    """
    Run game
    :param agents: list of agents
    :param environment: (optional) environment frame (example : mainWindow)
    :return:
    """
    initParameters(agents) # initialise game parameters

    if globals.gDebug:
        print('Writing log in ' + str(globals.gLogFileName) + '\n')

    while not globals.gEndGame:
        if globals.gDebug:
            print('\nCurrent iteration : ' + str(globals.gIteration))

        if globals.gLogData:
            writeLog(globals.gLogFileName, globals.gIteration, agents) # log data
        generateRandomSeeds(agents)

        if decisionProcess(agents):
            fscores = {agent.id : agent.score for agent in agents} # new
            endGame(agents)
            resetGame(agents)

            return fscores # new

def decisionProcess(agents):
    """
    Flip for each agent
    :param agents: list of agents
    :return: boolean, whether game ends
    """
    # continuous
    if globals.gContinuous:
        flipped = {}
        if globals.gIteration == 0:
            for agent in agents: # if first iteration, initialize all agents flip times
                agent.flipDecision(continuous=1)
                flipped[agent] = agent.flipTime
        else:
            for agent in agents: # if first iteration, initialize all agents flip times
                if agent.id != globals.gCurrentOwner.id:
                    flipped[agent] = agent.flipTime
                else:
                    globals.gCurrentOwner.flipDecision(continuous=1)
                    globals.gCurrentOwner.flipTime += globals.gIteration + globals.gPrec * np.random.random()
                    flipped[globals.gCurrentOwner] = globals.gCurrentOwner.flipTime

        globals.gIteration = min(min(flipped.values()), globals.gLastIteration)
        flipValue = globals.gIteration

        if globals.gIteration == globals.gLastIteration:
            flipped = {}

    # discrete
    else:
        flipped = {} # agents that flip or flip times for discrete/continuous respectively
        for agent in agents:
            agent.flipDecision()
            flipped[agent] = agent.flip
        globals.gIteration += 1
        flipValue = True

    if globals.gDebug:
        if flipped.values():
            flipsSt = 'Agents flip decisions : {'
            for ag,dec in flipped.items():
                flipsSt += 'Agent ' + str(ag.id) + ' : ' + str(dec) + ', '
            flipsSt = flipsSt[:-2] + '}'
            print(flipsSt)
        print('Current owner : ' + str(globals.gCurrentOwner.id))

    # if any agent flipped
    if any(flipped.values()):
        # add reward to current owner
        globals.gCurrentOwner.addReward()

        # update knowledge + add flip penalty
        flippedAgents = [agent for agent in flipped.keys() if flipped[agent] == flipValue]
        for agent in flippedAgents:
            globals.gGameFlips[agent.id].append(globals.gIteration)

        for agent in flippedAgents:
            agent.addPenalty()
            agent.updateKnowledge()

        # choose new owner at random
        agentOrder = np.random.permutation(flippedAgents)
        try:
            globals.gCurrentOwner = agentOrder[-1]
            if globals.gDebug:
                print('New owner : ' + str(globals.gCurrentOwner.id))
        except:
            pass

    # check if end of game
    if globals.gIteration >= globals.gLastIteration:
        globals.gCurrentOwner.addReward()
        return True

    return False