#!/usr/bin/env python
# -*- coding: utf-8 -*-

# path
import sys
from os import getcwd
sys.path.append(getcwd())

from gym import Env, spaces
from baselines import deepq
import numpy as np

from agents.agent import Agent
from config.properties import readProperties, setProperties
from config import globals

class flipItEnv(Env):
    """
    Define flipIt Environment
    """

    def __init__(self, agents):
        self.__version__ = "0.1.0"
        print("FlipIt Environment Version {}".format(self.__version__))

        # environment agents
        self.agents = agents
        self.dqnAgent = agents[0] # adaptive agent
        if self.dqnAgent.strategy != -1: # check if non-adaptive
            raise Exception('Agent 0 should be an adaptive agent (value -1).')

        # set  general variables defining the environment
        globals.gCurrentOwner = self.agents[globals.gCurrentOwnerId]
        self.TOTAL_TIME_STEPS = globals.gGameLength
        globals.gIteration = -1
        self.done = False

        # reinforcement learning variables (actions, observations)
        low = np.array([-self.TOTAL_TIME_STEPS, -1.0])
        high = np.array([self.TOTAL_TIME_STEPS + 1, self.TOTAL_TIME_STEPS + 1])
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        self.action_space = spaces.Discrete(2)  # Define what the agent can do, i.e. actions (flip, no flip

        # store what the agent tried
        self.curr_episode = -1
        self.action_episode_memory = []

    def step(self, action):
        """
        Step in the environment
        :param action: action to take at this step
        :return:
        """
        if self.done:
            raise RuntimeError("End of the Game")

        globals.gIteration += 1
        self._take_action(action)
        reward = self._get_reward() # reward given following the action
        ob = self._get_state() # get current state of game
        return ob, reward, self.done, {}

    def _take_action(self, action):
        """
        Action is the output from the RL algorithm
        :param action:
        :return:
        """
        flipped = {}  # agents that flip or flip times for discrete/continuous respectively
        for agent in agents:
            if agent.strategy == -1: # adaptive strategy
                flipped[agent] = action # 0 : don't flip, 1 : flip
            else:
                agent.flipDecision()
                flipped[agent] = agent.flip

        # if globals.gDebug:
        #     if flipped.values():
        #         flipsSt = 'Agents flip decisions : {'
        #         for ag, dec in flipped.items():
        #             flipsSt += 'Agent ' + str(ag.id) + ' : ' + str(dec) + ', '
        #         flipsSt = flipsSt[:-2] + '}'
        #         print(flipsSt)
        #     print('Current owner : ' + str(globals.gCurrentOwner.id))

        # if any agent flipped
        if any(flipped.values()):
            globals.gCurrentOwner.addReward() # add reward to current owner

            # update knowledge + add flip penalty
            flippedAgents = [agent for agent in flipped.keys() if flipped[agent]]
            for agent in flippedAgents:
                globals.gGameFlips[agent.id].append(globals.gIteration)

            for agent in flippedAgents:
                agent.updateKnowledge()
                agent.addPenalty()

            # choose new owner at random
            agentOrder = np.random.permutation(flippedAgents)
            try:
                globals.gCurrentOwner = agentOrder[-1]
                # if globals.gDebug:
                #     print('New owner : ' + str(globals.gCurrentOwner.id))
            except:
                pass

        # check if end of game
        if globals.gIteration >= self.TOTAL_TIME_STEPS:
            globals.gCurrentOwner.addReward()
            self.done = True
            print('END GAME. Scores : adaptive agent score = {}, non-adaptive agent score = {}'.format(self.agents[0].score, self.agents[1].score))

    def _get_reward(self):
        """
        Reward given after some action
        :return:
        """
        return self.dqnAgent.score - self.dqnAgent.prevScore

    def _get_state(self):
        """
        Get observation (agent's knowledge, time step)
        :return:
        """
        opponent_flip = self.dqnAgent.knowledge[1 - self.dqnAgent.id]
        return [opponent_flip, self.TOTAL_TIME_STEPS - globals.gIteration]

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.

        Returns
        -------
        observation (object): the initial observation of the space.
        """

        globals.gIteration = -1  # reset step counter
        for agent in self.agents:
            agent.reset()
        self.done = False # reset end of game
        self.action_episode_memory.append([])

        self.curr_episode += 1  # increase episode number
        return self._get_state() # get current state of game



def callback(lcl, _glb):
    """

    :param lcl:
    :param _glb:
    :return:
    """
    # stop training if reward exceeds 199
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 1000
    return is_solved


if __name__ == '__main__':
    setProperties(readProperties('../config/parameters/dqn.properties'))

    agents = [Agent(strategy=-1, type='LM'), Agent(strategy=0, strategyParam=0.02)]
    env = flipItEnv(agents)
    act = deepq.learn(
        env,
        network='mlp',
        lr=1e-3,
        total_timesteps=100000,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        print_freq=10,
        callback=callback
    )
