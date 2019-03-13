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
        self.DQNAgent = agents[0] # adaptive agent
        if self.DQNAgent.strategy != -1: # check if non-adaptive
            raise Exception('Agent 0 should be an adaptive agent (strategy -1).')
        self.oppAgent = agents[1]

        # set  general variables defining the environment
        self.done = False
        self.currStep = -1
        self.steps = globals.gGameLength
        self.flipCost = globals.gFlipCost
        self.flipReward = globals.gFlipReward

        # reinforcement learning variables (actions, observations)
        #low = np.array([0, 0, 0])
        #high = np.array([self.steps + 1, self.steps + 1, 2])
        #self.observation_space = spaces.Box(low, high, dtype=np.float32)

        self.observation_space = spaces.Discrete(self.steps + 1) # time since last flip
        #self.observation_space = spaces.Discrete(2) # owner or not
        self.action_space = spaces.Discrete(2)  # defines what the agent can do, i.e. actions (flip, don't flip)

        # store what the agent tried
        self.currEpisode = -1
        self.actionEpisodeMemory = []

        self.flips = []

    def step(self, action):
        """
        Step in the environment
        :param action: action to take at this step
        :return:
        """
        if self.done:
            raise RuntimeError("End of the Game")

        self.currStep += 1

        reward = self._take_action(action)
        ob = self._get_state(knownOwner=action)  # get current state of game

        # print(action, ob, reward)
        return ob, reward, self.done, {}

    def _take_action(self, action):
        """
        Take action and return adaptive agent's reward
        :param action: action to take
        :return: reward achieved by the action
        """
        flipped = {}  # agents that flip or flip times for discrete/continuous respectively

        for agent in agents:
            if agent.strategy == -1: # adaptive strategy : don't flip (0) or flip (1)
                flipped[agent] = action
                if action:
                    self.flips.append(self.currStep)
            else:
                globals.gIteration = self.currStep
                agent.flipDecision() # run corresponding strategy
                flipped[agent] = agent.flip
                if agent.flip:
                    agent.lastFlipTime = self.currStep


            # update score : if flip, add flip Cost, if current owner, add owner Reward
            score = agent.isCurrentOwner() * self.flipReward - flipped[agent] * self.flipCost
            agent.score += score
            if agent.strategy == -1:
                actionReward = score

        # if any agent flipped, update game and choose new resource owner
        if any(flipped.values()):
            flippedAgents = [agent for agent in flipped.keys() if flipped[agent]] # get agents that flipped

            # update game flips vector
            for agent in flippedAgents:
                globals.gGameFlips[agent.id].append(self.currStep)

            # update agents' knowledge
            for agent in flippedAgents:
                agent.updateKnowledge()

            # choose new owner at random
            # agentOrder = np.random.permutation(flippedAgents)
            # agentOrder[-1].setCurrentOwner()

            # give priority to DQN agent
            self.DQNAgent.setCurrentOwner()

        # end of game
        if self.currStep >= self.steps:
            self.done = True
            print('Episode {} : adaptive agent score = {}, non-adaptive agent score = {}'.format(self.currEpisode, self.agents[0].score, self.agents[1].score))
            print(self.flips)

        return actionReward

    def _get_state(self, knownOwner):
        """
        Get observation (agent's knowledge, time step)
        :return:
        """
        opponentFlipTime = self.DQNAgent.knowledge[1 - self.DQNAgent.id]
        if opponentFlipTime:
            return self.currStep - opponentFlipTime
        return self.currStep

        # opponentFlipTime = self.DQNAgent.knowledge[1 - self.DQNAgent.id]
        # return [opponentFlipTime, self.currStep, self.DQNAgent.isCurrentOwner()]

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.

        Returns
        -------
        observation (object): the initial observation of the space.
        """
        globals.gGameFlips = {idx: [] for idx in range(globals.gNbAgents)}

        self.flips = []
        self.currStep = -1  # reset step counter
        for agent in self.agents:
            agent.reset()

        self.DQNAgent.setCurrentOwner()
        self.done = False  # reset end of game
        self.actionEpisodeMemory.append([])

        self.currEpisode += 1  # increase episode number
        return self._get_state(knownOwner=1)  # get current state of game, DQN initial owner of the game


def callback(lcl, _glb):
    """

    :param lcl:
    :param _glb:
    :return:
    """
    # stop training if reward exceeds 199
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 0
    return is_solved


if __name__ == '__main__':
    setProperties(readProperties('../config/parameters/dqn.properties'))

    # Agents
    DQNAgent = Agent(strategy=-1, type='LM')
    DQNAgent.setCurrentOwner()
    oppAgent = Agent(strategy=0, strategyParam=0.05)
    agents = [DQNAgent, oppAgent]

    # Environment
    env = flipItEnv(agents)

    # Training
    act = deepq.learn(
        env,
        network='mlp',
        lr=0.001,
        total_timesteps=100000,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.002,
        batch_size=32,
        print_freq=10,
        gamma=1,
        prioritized_replay=True,
    )
