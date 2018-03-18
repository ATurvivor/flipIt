#!/usr/bin/env python

from ext import globals

def readProperties(propertiesFile):
    """
    Reads properties file
    :param propertiesFile: properties file name
    :return: dictionary containing all properties and their corresponding values
    """
    f = open(propertiesFile, 'r')
    file = f.readlines()

    properties = {}

    for line in file:
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
    globals.gIteration = 0

    globals.gLogFileName = None
    globals.gLogData = eval(properties['gLogData'])

    globals.gDebug = eval(properties['gDebug'])

    globals.gNbAgents = eval(properties['gNbAgents'])
    globals.gAgentId = eval(properties['gAgentId'])
    globals.gFlipCost = eval(properties['gFlipCost'])
    globals.gFlipReward = eval(properties['gFlipReward'])
    globals.gRandomSeeds = {}

    # Game globals
    globals.gEnvironment = eval(properties['gEnvironment'])
    globals.gCurrentTime = eval(properties['gCurrentTime'])
    globals.gEndGameProbability = eval(properties['gEndGameProbability'])
    globals.gEndGame = eval(properties['gEndGame'])
    #globals.gCurrentOwner = eval(properties['gCurrentOwner'])

if __name__ == '__main__':
    fileName = 'test.properties'
    prop = readProperties(fileName)
    setProperties(prop)
    print(globals.gLogData)