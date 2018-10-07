#!/usr/bin/env python

from endGame import *
from config.log import initLogFileName, writeLog

import numpy as np


def initParameters():
    """
    Initialises game parameters
    :param environment:
    :return:
    """
    globals.gLogFileName = initLogFileName() # initialise log file name
    globals.gAgentStartId = 0

    if globals.gFiniteTime == 1: # finite
        globals.gGameEnd = globals.gLastIteration
    elif globals.gGameType == 0: # infinite and continuous
        globals.gGameEnd = np.random.exponential(scale=1.0 / globals.gEndGameProbability)
    else: # infinite and discrete
        globals.gGameEnd = np.random.geometric(p=globals.gEndGameProbability)

def run_simulation(agents):
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

        writeLog(globals.gLogFileName, globals.gIteration, agents) # log data
        generateRandomSeeds(agents)

        if decisionProcess(agents):
            endGame(agents)
            resetGame(agents)

def run_environment(env, agents):
    """

    :param agents:
    :param env:
    :return:
    """
    if not globals.gEndGame:
        if globals.gDebug:
            print('\nCurrent iteration : ' + str(globals.gIteration))

        env.root.upperFrame.displayRun()

        writeLog(globals.gLogFileName, globals.gIteration, agents) # log data
        generateRandomSeeds(agents)

        if decisionProcess(agents, env):
            env.updateBoard()

        if not globals.gInteractive:
            env.updateScore()

    env._job = env.after(50, env.run, agents)

def generateRandomSeeds(agents):
    """
    Generates random seeds for each agent
    :param agents: list of agents
    :return:
    """
    globals.gRandomSeeds = {agent.id:np.random.uniform(0, 1.0) for agent in agents}

def decisionProcess(agents, env=None):
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
    elif (env and env.getGameType()) or (not env and globals.gGameType):
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
        print('New owner : ' + str(globals.gCurrentOwner.id))

        # add flip on board
        if env:
            if globals.gCurrentOwner.id != 0 or (globals.gCurrentOwner.id == 0 and globals.gCurrentOwner.strategy.get() != 3):
                env.root.upperFrame.addFlip(globals.gCurrentOwner)
            if globals.gCurrentOwner.id == 0 and globals.gInteractive:
                env.updateScore()


    return False

def updateScores(fAgents):
    """
    Updates scores
    :param fAgents: list of agents who flipped
    :return:
    """
    globals.gCurrentOwner.addReward()
    for agent in fAgents:
        agent.addPenalty()
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

