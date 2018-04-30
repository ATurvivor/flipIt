#!/usr/bin/env python

from endGame import *
# globals and log imported from endGame
import numpy as np
from config.log import writeLog
from config.init import initGame


def run(agents, environment=None):
    """
    Run game
    :param agents: list of agents
    :param environment: (optional) environment frame (example : mainWindow)
    :return:
    """
    initGame() # initialise game parameters

    if globals.gDebug:
        print('Writing log in ' + str(globals.gLogFileName) + '\n')

    while not globals.gEndGame:
        if globals.gDebug:
            print('\nCurrent iteration : ' + str(globals.gIteration))

        if environment:
            environment.root.upperFrame.displayRun()

        writeLog(globals.gLogFileName, globals.gIteration, agents) # log data
        generateRandomSeeds(agents)
        if decisionProcess(agents):
            endGame(agents)
            resetGame(agents)


def generateRandomSeeds(agents):
    """
    Generates random seeds for each agent
    :param agents: list of agents
    :return:
    """
    globals.gRandomSeeds = {agent.id:np.random.uniform(0, 1.0) for agent in agents}

def decisionProcess(agents, environment=None):
    """
    Flip for each agent
    :param agents: list of agents
    :return: boolean, whether game ends
    """
    # continuous
    if globals.gGameType == 0:
        flipped = globals.gFlipped
        if globals.gIteration == 0.0: # first iteration
            for agent in agents: # initialize all agents flip times
                agent.flipDecision(gameType=0)
                flipped[agent] = agent.flipTime
        else:
            # TODO fix collisions
            # Updates only previous owners flip time
            # This method doesn't yet work for continuous collisions
            globals.gCurrentOwner.flipDecision(gameType=0)
            flipped[globals.gCurrentOwner] = globals.gCurrentOwner.flipTime + globals.gIteration+globals.gPrec*np.random.random()

        globals.gFlipped = flipped
        globals.gIteration = np.minimum(np.amin(flipped.values()), globals.gGameEnd)
        flipValue = globals.gIteration

    # discrete
    elif (environment and environment.gameTypeFrame.type.get() == 1) or (not environment and globals.gGameType == 1):
        flipped = {} # agents that flip or flip times for discrete/continuous respectively
        for agent in agents:
            if (globals.gInteractive and agent.id != 0) or not globals.gInteractive: # any agent that is not human
                agent.flipDecision(1)
            flipped[agent] = agent.flip
        globals.gIteration += 1
        flipValue = True

    if globals.gDebug:
        print('Agents flip decisions : ' + str(flipped))
        print('Current owner : ' + str(globals.gCurrentOwner.id))

    # check if end of game
    if globals.gIteration >= globals.gGameEnd:
        globals.gCurrentOwner.addReward()
        return True

    # choose next owner
    if any(flipped.values()):
        # if one or more agents flipped, pick random
        flippedAgents = [agent for agent in flipped.keys() if flipped[agent] == flipValue]
        updateScores(flippedAgents)
        updateCurrentOwner(flippedAgents)

        # add flip on board
        if environment:
            environment.parent.upperFrame.addFlip(globals.gCurrentOwner)

    return False

def updateScores(fAgents):
    """
    Updates scores
    :param fAgents: list of agents who flipped
    :return:
    """
    globals.gCurrentOwner.addReward()
    for agent in fAgents:
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

