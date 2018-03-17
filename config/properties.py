from ext import globals

fileName = 'test.properties'

def readProperties(propertiesFile):
    """
    Reads config
    :param propertiesFile: property file name
    :return: dictionary containing config and their values
    """
    f = open(propertiesFile, 'r')
    file = f.readlines()

    properties = {}

    for line in file:
        if '=' in line:
            sp = line.split(' = ')
            properties[sp[0]] = sp[1]
    f.close()
    return properties

def setProperties(properties):
    """
    Sets config to global variables
    :param globalsFile:
    :param properties:
    :return:
    """

    # Data
    globals.gLogData = eval(properties['gLogData'])

    # Agents
    globals.gAgentId = eval(properties['gAgentId'])

    # Game globals
    globals.gEnvironment = eval(properties['gEnvironment'])
    globals.gCurrentTime = eval(properties['gCurrentTime'])
    globals.gEndGameProbability = eval(properties['gEndGameProbability'])
    globals.gEndGame = eval(properties['gEndGame'])

if __name__ == '__main__':
    prop = readProperties(fileName)
    setProperties(prop)
    print(globals.gLogData)