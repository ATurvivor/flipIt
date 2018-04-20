#!/usr/bin/env python

import numpy as np
from config import globals


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
    globals.gIteration = 0.0

    globals.gLogFileName = eval(properties['gLogFileName'])
    globals.gLogData = eval(properties['gLogData'])

    globals.gDebug = eval(properties['gDebug'])

    globals.gAgentStartId = eval(properties['gAgentStartId'])
    globals.gNbAgents = eval(properties['gNbAgents'])
    globals.gFlipCost = eval(properties['gFlipCost'])
    globals.gFlipReward = eval(properties['gFlipReward'])
    globals.gRandomSeeds = {}

    # Game globals
    globals.gEnvironment = eval(properties['gEnvironment'])
    globals.gInteractive = eval(properties['gInteractive'])
    globals.gCurrentOwner = eval(properties['gCurrentOwner'])

    globals.gCurrentTime = eval(properties['gCurrentTime'])
    globals.gFiniteTime = eval(properties['gFiniteTime'])
    globals.gGameType = eval(properties['gGameType'])

    globals.gEndGameProbability = eval(properties['gEndGameProbability'])
    globals.gEndGame = eval(properties['gEndGame'])

    globals.gLastIteration = eval(properties['gLastIteration'])

    globals.gGameFlips = [[] for _ in range(globals.gNbAgents)]
    globals.gFlipped = {}
