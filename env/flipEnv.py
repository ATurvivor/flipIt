#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simulate the simplifie Banana selling environment.

Each episode is selling a single banana.
"""

# core modules
import logging.config
import math
import pkg_resources
import random

# 3rd party modules
from gym import spaces
import gym
import numpy as np


from simulations.run import initParameters
from agents.agent import Agent
from config.properties import readProperties, setProperties
from config import globals

def decisionProcess(agents):
    """
    Flip for each agent
    :param agents: list of agents
    :return: boolean, whether game ends
    """
    flipped = {} # agents that flip or flip times for discrete/continuous respectively
    for agent in agents:
        agent.flipDecision(continuous=0)
        flipped[agent] = agent.flip
    globals.gIteration += 1
    flipValue = True

    if globals.gDebug:
        if flipped.values():
            flipsSt = 'Agents flip decisions : {'
            for ag,dec in flipped.items():
                flipsSt += 'Agent ' + str(ag.id) + ' : ' + str(dec) + ', '
            flipsSt = flipsSt[:-2] + '}'
            print(flipsSt)
        print('Current owner : ' + str(globals.gCurrentOwner.id))

    # if any agent flipped
    if any(flipped.values()):
        # add reward to current owner
        globals.gCurrentOwner.addReward()

        # update knowledge + add flip penalty
        flippedAgents = [agent for agent in flipped.keys() if flipped[agent] == flipValue]
        for agent in flippedAgents:
            globals.gGameFlips[agent.id].append(globals.gIteration)

        for agent in flippedAgents:
            agent.addPenalty()
            agent.updateKnowledge()

        # choose new owner at random
        agentOrder = np.random.permutation(flippedAgents)
        try:
            globals.gCurrentOwner = agentOrder[-1]
            if globals.gDebug:
                print('New owner : ' + str(globals.gCurrentOwner.id))
        except:
            pass

    # check if end of game
    if globals.gIteration >= globals.gLastIteration:
        globals.gCurrentOwner.addReward()
        return True

    return False


class flipItEnv(gym.Env):
    """
    Define flipIt Environment
    """

    def __init__(self, agent):
        self.__version__ = "0.1.0"
        print("FlipIt Environment Version {}".format(self.__version__))

        self.agent = agent

        # General variables defining the environment
        self.TOTAL_TIME_STEPS = globals.gGameLength

        self.curr_step = -1
        self.is_end_of_game = globals.gEndGame
        self.action_space = spaces.Discrete(2) # Define what the agent can do, i.e. actions (flip, no flip)

        # Observation is the remaining time
        low = np.array([0.0,  ]) # remaining_tries
        high = np.array([self.TOTAL_TIME_STEPS,  ]) # remaining_tries
        self.observation_space = spaces.Box(low, high, dtype=np.float32) # TODO revoir

        # Store what the agent tried
        self.curr_episode = -1
        self.action_episode_memory = []

    def step(self, action):
        """
        The agent takes a step in the environment.

        Parameters
        ----------
        action : int

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        if self.is_end_of_game:
            raise RuntimeError("End of the Game")
        self.curr_step += 1
        self._take_action(action)
        reward = self._get_reward()
        ob = self._get_state()
        return ob, reward, self.is_end_of_game, {}

    def _take_action(self, action):

        self.action_episode_memory[self.curr_episode].append(action)
        self.price = ((float(self.MAX_PRICE) /
                      (self.action_space.n - 1)) * action)

        chance_to_take = 0 #get_chance(self.price)
        banana_is_sold = (random.random() < chance_to_take)

        if banana_is_sold:
            self.is_banana_sold = True

        remaining_steps = self.TOTAL_TIME_STEPS - self.curr_step
        time_is_over = (remaining_steps <= 0)
        throw_away = time_is_over and not self.is_banana_sold
        if throw_away:
            self.is_banana_sold = True  # abuse this a bit
            self.price = 0.0

    def _get_reward(self):
        """Reward is given for a sold banana."""
        if self.is_banana_sold:
            return self.price - 1
        else:
            return 0.0

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.

        Returns
        -------
        observation (object): the initial observation of the space.
        """
        self.curr_step = -1
        self.curr_episode += 1
        self.action_episode_memory.append([])
        self.is_banana_sold = False
        self.price = 1.00
        return self._get_state()

    def _render(self, mode='human', close=False):
        return

    def _get_state(self):
        """Get the observation."""
        ob = [self.TOTAL_TIME_STEPS - self.curr_step]
        return ob

    def seed(self, seed):
        random.seed(seed)
        np.random.seed


if __name__ == '__main__':
    setProperties(readProperties('config/parameters/test.properties'))

    agents = [Agent(strategy=0), Agent(strategy=0)]
    initParameters(agents)


    dqnAgent = agents[0]
    flipIt = flipItEnv(dqnAgent)