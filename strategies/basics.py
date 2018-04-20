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

    if gameType == 0:
        agent.flipTime = -1.0 / p * np.log(globals.gRandomSeeds[agent.id])
    elif globals.gRandomSeeds[agent.id] < p:
        agent.flip = True


def periodic(agent, gameType):
    """
    Deterministic periodic strategy
    :param agent: agent executing strategy
    :return: tuple of form (discrete response, continuous response)
    """
    per = 1.0 / agent.strategyParam
    agent_history = [globals.gGameFlips[i][:agent.perspectiveHistory[i]] for i in globals.gNbAgents] # TODO modify range to agents

    if gameType == 0: # continuous
        agent.flipTime = per
    elif globals.gIteration-agent_history[agent.id][-1] > per: # discrete
        agent.flip = True


def delayedRandomDecayed(agent, gameType):
    """
    Exponential decay/Geometric distribution memoryless strategy except with automatic delay
    :param agent: agent executing strategy
    :return: tuple of form (discrete response, continuous response)
    """
    p, delay = agent.strategyParam
    agent_history = [globals.gGameFlips[i][:agent.perspectiveHistory[i]] for i in globals.gNbAgents]

    if gameType == 0: # continuous
        agent.flipTime = delay - 1.0 / p * np.log(globals.gRandomSeeds[agent.id])
    elif globals.gRandomSeeds[agent.id] < p and globals.gIteration - agent_history[agent.id][-1] > delay:
        agent.flip = True
