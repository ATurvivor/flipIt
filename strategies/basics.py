import numpy as np
from ext import globals


def run_strategy(agent):
    """
    Runs strategy based on strategy code integer
    :param agent:
    :return:
    """

    strategies={0:randomDecayed, 1:periodic, 2:delayedRandomDecayed}
    if globals.gEnvironment:
        return strategies[agent.strategy.get()](agent)
    return strategies[agent.strategy](agent)

def randomDecayed(agent):
    """
    Exponential decay/Geometric distribution memoryless strategy
    :param agent: agent executing strategy
    :return: tuple of form (discrete response, continuous response)
    """
    p=agent.strategyParam
    if globals.gRandomSeeds[agent.id] < p:
        agent.flip = True
    agent.flipTime = -1.0 / p * np.log(globals.gRandomSeeds[agent.id])
    return agent.flip, agent.flipTime

def periodic(agent):
    """
    Deterministic periodic strategy
    :param agent: agent executing strategy
    :return: tuple of form (discrete response, continuous response)
    """

    per=1.0/agent.strategyParam
    agent_history=[globals.gGameFlips[i][:agent.perspectiveHistory[i]] for i in globals.gNbAgents]
    if globals.gIteration-agent_history[agent.id][-1] >per:
        agent.flip = True
    agent.flipTime = per
    return agent.flip, agent.flipTime

def delayedRandomDecayed(agent):
    """
    Exponential decay/Geometric distribution memoryless strategy except with automatic delay
    :param agent: agent executing strategy
    :return: tuple of form (discrete response, continuous response)
    """

    p,delay=agent.strategyParam
    agent_history=[globals.gGameFlips[i][:agent.perspectiveHistory[i]] for i in globals.gNbAgents]
    if globals.gRandomSeeds[agent.id] < p and globals.gIteration-agent_history[agent.id][-1]>delay:
        agent.flip = True
    agent.flipTime = delay -1.0 / p * np.log(globals.gRandomSeeds[agent.id])
    return agent.flip, agent.flipTime
