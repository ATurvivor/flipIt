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
        decisionProcess(agents)
        verifyEndGame(agents)

        globals.gIteration += 1


def generateRandomSeeds(agents):
    """
    Generates random seeds for each agent
    :param agents: list of agents
    :return:
    """
    globals.gRandomSeeds = {agent.id:np.random.uniform(0,0.05) for agent in agents}

def decisionProcess(agents):
    """
    Flip for each agent
    :param agents: list of agents
    :return:
    """
    flipped = {}
    for agent in agents:
        flipped[agent] = agent.flipDecision()

    if globals.gDebug:
        print('Agents flip decisions : ' + str(flipped.values()))

    if any(flipped.values()):
        # if one or more agents flipped, pick random
        flippedAgents = [agent for agent in flipped.keys() if flipped[agent]]
        updateScores(flippedAgents)
        updateCurrentOwner(flippedAgents)


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
    globals.gCurrentOwner = np.random.choice(agents)