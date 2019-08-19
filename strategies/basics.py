import numpy as np
from config import globals
import math


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

def periodic_with_random_phase(agent, continuous):
    """

    :param agent:
    :param continuous:
    :return:
    """
    per = 1.0 / agent.strategyParam
    if globals.gIteration > per:
        periodic(agent, continuous)
    elif np.random.random() < 0.5: # random phase
        agent.flip = False
    else:
        agent.flip = True

def exponential(agent, continuous):
    """

    :param agent: agent executing strategy
    :param continuous: True if continuous, false otherwise (discrete)
    :return:
    """
    p = agent.strategyParam

    if continuous:
        agent.flipTime = np.random.exponential(scale=1.0/p)
    elif np.random.random() < p:
        agent.flip = True
    else:
        agent.flip = False

def delayedExponential(agent, continuous):
    """
    Delayed exponential memoryless strategy
    :param agent:
    :param continuous:
    :return:
    """
    p, delay = agent.strategyParam
    delay = 1.0 / delay

    if continuous:
        agent.flipTime = delay + np.random.exponential(scale=1.0/p)
    elif np.random.random() < p and globals.gIteration - agent.lastFlipTime >= delay:
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

def idle(agent, continuous):
    """
    Idle strategy
    :param agent:
    :param continuous:
    :return:
    """
    if continuous:
        agent.flipTime = -1 # TODO check
    else:
        agent.flip = False

def greedy(agent, continous, op_agent):
    """
    :param agent: 
    :param continuous:
    :param oppo_agent: the opponent 
    """
    
    if agent.type != 'LM' :  # check if Last Move
        raise Exception('Greedy agent should be an LM player (type = LM).')
    
    try: # if opponent did not flip, this would return an error
        tao = agent.knowledge[1-agent.id] # op_lastfliptime
    except:
        if np.random.random() < 0.5: # random phase
            agent.flip = False
        else:
            agent.flip = True
        return     
        
    k1 = globals.gFlipCost / globals.gFlipReward 
    
    L_z = 0.0 # local benefit
    max_L_z = -1.0
    max_z = -1.0
        
    if op_agent.strategy == 0: # periodic
        #assumption: greedy_cost (k1) < op_agent.strategyParam/2
        op_per = 1.0/op_agent.strategyParam # delta
        for z in range(0, globals.gGameLength-globals.gIteration+1): # interval candidate
            if z >= op_per - tao:
                L_z = (op_per-tao-k1)/z
            else:
                L_z = 1-k1/z
            if L_z > max_L_z:
                max_L_z = L_z
                max_z = z
        if continous and max_L_z > 0:
            agent.flipTime = globals.gIteration + max_z
        elif max_L_z > 0 and max_z == 0:
            agent.flip = True
        else:
            agent.flip = False
            
    #elif op_agent.strategy == 1: # uniform
        # agent.strategyParam 
    elif op_agent.strategy == 3: # exponential
        lambda_ = op_agent.strategyParam
        for z in range(0, globals.gGameLength-globals.gIteration+1):
            L_z = (1-math.exp(0-lambda_*z))/(lambda_*z)-k1/z
            if L_z > max_L_z:
                max_L_z = L_z
                max_z = z
        if continous and max_L_z > 0:
            agent.flipTime = globals.gIteration + max_z
        elif max_L_z > 0 and max_z == 0:
            agent.flip = True
        else:
            agent.flip = False
            
    else:
        raise Exception('unimplemented (not periodic 0, (uniform 1) or exponential 3)')
    
     
    
