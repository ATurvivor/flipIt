import numpy as np
from config import globals


def periodic(agent, continuous):
    """
    Deterministic periodic strategy
    :param agent: agent executing strategy
    :param continuous: True if continuous, false otherwise (discrete)
    :return:
    """
    per = 1.0 / agent.strategyParam
    if continuous:
        agent.flipTime = per
    elif globals.gIteration - agent.lastFlipTime >= per:
        agent.flip = True
    else:
        agent.flip = False


def exponential(agent, continuous):
    """

    :param agent: agent executing strategy
    :param continuous: True if continuous, false otherwise (discrete)
    :return:
    """
    p = agent.strategyParam

    if continuous:
        agent.flipTime = np.random.exponential(scale=1.0/p)
    elif np.random.geometric(p) == 1:
        agent.flip = True
    else:
        agent.flip = False

def delayedExponential(agent, continuous):
    """

    :param agent:
    :param continuous:
    :return:
    """
    p, delay = agent.strategyParam
    delay = 1.0 / delay

    if continuous:
        agent.flipTime = delay + np.random.exponential(scale=1.0/p)
    elif np.random.geometric(p) == 1 and globals.gIteration - agent.lastFlipTime >= delay:
        agent.flip = True
    else:
        agent.flip = False


def uniform(agent, continuous):
    """
    Exponential decay/Geometric distribution memoryless strategy
    :param agent: agent executing strategy
    :param continuous: True if continuous, false otherwise (discrete)
    :return: tuple of form (discrete response, continuous response)
    """
    p = agent.strategyParam

    if continuous:
        agent.flipTime = np.random.exponential(scale=1.0/p)
    elif np.random.random() < p:
        agent.flip = True
    else:
        agent.flip = False


def delayedUniform(agent, continuous):
    """
    Exponential decay/Geometric distribution memoryless strategy except with automatic delay
    :param agent: agent executing strategy
    :param continuous: true if continuous, false otherwise (discrete)
    :return: tuple of form (discrete response, continuous response)
    """
    p, delay = agent.strategyParam
    delay = 1.0 / delay

    if continuous:
        agent.flipTime = delay + np.random.exponential(scale=1.0/p)
    elif np.random.random() < p and globals.gIteration - agent.lastFlipTime >= delay:
        agent.flip = True
    else:
        agent.flip = False

