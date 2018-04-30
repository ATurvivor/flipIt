import numpy as np

from config import globals


def run_strategy(agent, gameType):
    """
    Runs strategy based on strategy code integer
    :param gameType: continuous or discrete
    :param agent: Agent
    :return:
    """
    strategies = {0 : randomDecayed, 1 : periodic, 2 : delayedRandomDecayed}
    if globals.gEnvironment:
        return strategies[agent.strategy.get()](agent, gameType)
    return strategies[agent.strategy](agent, gameType)


def randomDecayed(agent, gameType):
    """
    Exponential decay/Geometric distribution memoryless strategy
    :param agent: agent executing strategy
    :return: tuple of form (discrete response, continuous response)
    """
    p = agent.strategyParam
    used_hist=np.zeros((globals.gNbAgents,1))
    hist=1
    agent_history = np.zeros((globals.gNbAgents, hist))
    for ag in range(globals.gNbAgents):
        for idx in range(np.minimum(int(agent.perspectiveHistory[ag]),hist)):
            agent_history[ag,-idx-1]=globals.gGameFlips[ag][int(agent.perspectiveHistory[ag])-idx-1]
    if gameType == 0:
        agent.flipTime = np.random.exponential(scale=1.0/p)
        print(agent.flipTime)
    elif np.random.random() < p:
        agent.flip = True
    else:
        agent.flip = False


def periodic(agent, gameType):
    """
    Deterministic periodic strategy
    :param agent: agent executing strategy
    :return: tuple of form (discrete response, continuous response)
    """
    per = 1.0 / agent.strategyParam
    hist=1
    agent_history = np.zeros((globals.gNbAgents, hist))
    for ag in range(globals.gNbAgents):
        for idx in range(np.minimum(int(agent.perspectiveHistory[ag]),hist)):
            agent_history[ag,-idx-1]=globals.gGameFlips[ag][int(agent.perspectiveHistory[ag])-idx-1]
    if gameType == 0: # continuous
        agent.flipTime = per
    elif globals.gIteration - agent_history[agent.id][0] >= per:
        agent.flip = True
    else:
        agent.flip = False

def delayedRandomDecayed(agent, gameType):
    """
    Exponential decay/Geometric distribution memoryless strategy except with automatic delay
    :param agent: agent executing strategy
    :return: tuple of form (discrete response, continuous response)
    """
    if(globals.gEnvironment):
        p, delay = .01,.01
    else:
        p, delay = agent.strategyParam
    delay=1.0/delay
    hist=1
    agent_history = np.zeros((globals.gNbAgents, hist))
    for ag in range(globals.gNbAgents):
        for idx in range(np.minimum(int(agent.perspectiveHistory[ag]),hist)):
            agent_history[ag,-idx-1]=globals.gGameFlips[ag][int(agent.perspectiveHistory[ag])-idx-1]
    if gameType == 0: # continuous
        agent.flipTime = delay + np.random.exponential(scale=1.0/p)
        print(agent.flipTime)
    elif np.random.random() < p and globals.gIteration - agent_history[agent.id][0] >= delay:
        agent.flip = True
    else:
        agent.flip = False

