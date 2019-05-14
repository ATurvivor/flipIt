#!/usr/bin/env python

from config import globals
from config.log import initLog


def readProperties(propertiesFile):
    """
    Reads properties file
    :param propertiesFile: properties file name
    :return: dictionary containing all properties and their corresponding values
    """
    f = open(propertiesFile, 'r')
    data = f.readlines()

    properties = {}

    for line in data:
        line = line.split(' #')[0]
        if '=' in line and line[0] != '#':
            sp = line.split(' = ')
            properties[sp[0]] = sp[1]
    f.close()
    return properties

def setProperties(properties):
    """
    Sets config to global variables
    :param globalsFile: file containing global variables
    :param properties: properties dictionary
    :return:
    """
    # Data log
    globals.gLogFileName = eval(properties['gLogFileName'])
    if not globals.gLogFileName:
        globals.gLogFileName = initLog()
    globals.gLogData = eval(properties['gLogData'])

    globals.gDebug = eval(properties['gDebug'])

    # Game globals
    globals.gIteration = 0.0
    globals.gEnvironment = eval(properties['gEnvironment'])
    globals.gInteractive = eval(properties['gInteractive'])
    globals.gCurrentOwnerId = eval(properties['gCurrentOwnerId'])

    # Agents
    globals.gAgentStartId = eval(properties['gAgentStartId'])
    globals.gNbAgents = eval(properties['gNbAgents'])
    globals.gFlipCost = eval(properties['gFlipCost'])
    globals.gFlipReward = eval(properties['gFlipReward'])
    globals.gRandomSeeds = {}

    # Variations of the Game
    globals.gFiniteTime = eval(properties['gFiniteTime'])
    globals.gContinuous = eval(properties['gContinuous'])

    globals.gEndGameProbability = eval(properties['gEndGameProbability'])
    globals.gEndGame = eval(properties['gEndGame'])
    globals.gGameLength = eval(properties['gGameLength'])
    globals.gLastIteration = eval(properties['gGameLength'])
    globals.gPrec = eval(properties['gPrec'])

    globals.gGameFlips = {idx : [] for idx in range(globals.gNbAgents)}
    globals.gFlipped = {}
