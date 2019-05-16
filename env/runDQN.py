# path
import sys
from os import getcwd

sys.path.append(getcwd())

import torch
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from gym import Env, spaces
from datetime import datetime

from agents.agent import Agent
from agents.dqnAgent import dqnAgent

from config.properties import readProperties, setProperties
from config import globals

class flipIt(Env):
    """
    Define flipIt Environment
    """

    def __init__(self):
        self.__version__ = "0.1.0"
        print("FlipIt Environment Version {}".format(self.__version__))

        # set general variables defining the environment
        self.done = False
        self.currStep = -1
        self.steps = globals.gGameLength
        self.flipCost = globals.gFlipCost
        self.flipReward = globals.gFlipReward

        # obs/action space
        low = np.array([0, 0])
        high = np.array([self.steps + 1, self.steps + 1])
        self.observation_space = spaces.Box(low, high, dtype=np.int32)
        self.action_space = spaces.Discrete(2)  # defines what the agent can do, i.e. actions (flip, don't flip)

        self.state_size = self.observation_space.shape[0]
        self.action_size = self.action_space.n

        # agents
        self.dqn = dqnAgent(action_size=self.action_size, state_size=self.state_size, seed=0)  # adaptive agent
        if self.dqn.strategy != -1:  # check if non-adaptive
            raise Exception('Agent 0 should be an adaptive agent (strategy -1).')
        self.dqn.setCurrentOwner()  # initial owner
        self.opp = Agent(strategy=0, strategyParam=0.05)

        self.agents = [self.dqn, self.opp]

        self.flips = []
        self.oppFlips = []

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
        ob = self._get_state()  # get current state of game

        return ob, reward, self.done, {}

    def _take_action(self, action):
        """
        Take action and return adaptive agent's reward
        :param action: action to take
        :return: reward achieved by the action
        """
        flipped = {}  # agents that flip or flip times for discrete/continuous respectively

        for agent in self.agents:
            if agent.strategy == -1:  # adaptive strategy : don't flip (0) or flip (1)
                flipped[agent] = action
                if action:
                    agent.lastFlipTime = self.currStep
                    self.flips.append(self.currStep)
            else:
                globals.gIteration = self.currStep
                agent.flipDecision()  # run corresponding strategy
                flipped[agent] = agent.flip
                if agent.flip:
                    agent.lastFlipTime = self.currStep
                    self.oppFlips.append(self.currStep)

            # update score : if flip, add flip Cost, if current owner, add owner Reward
            score = agent.isCurrentOwner() * self.flipReward - flipped[agent] * self.flipCost
            agent.score += score
            if agent.strategy == -1:
                actionReward = score

        # if any agent flipped, update game and choose new resource owner
        if any(flipped.values()):
            flippedAgents = [agent for agent in flipped.keys() if flipped[agent]]  # get agents that flipped

            # update game flips vector
            for agent in flippedAgents:
                globals.gGameFlips[agent.id].append(self.currStep)

            # update agents' knowledge
            for agent in flippedAgents:
                agent.updateKnowledge()

            # choose new owner at random
            # agentOrder = np.random.permutation(flippedAgents)
            # agentOrder[-1].setCurrentOwner()

            if len(flippedAgents) == 1:
                flippedAgents[0].setCurrentOwner()
            else:
                # give priority to DQN agent if both flipped
                self.dqn.setCurrentOwner()
                # self.oppAgent.setCurrentOwner()

        # end of game
        if self.currStep >= self.steps:
            self.done = True

        return actionReward

    def _get_state(self):
        """
        Get observation
        :return:
        """
        if self.opp.strategy == 0: # periodic
            opponentFlipTime = self.dqn.knowledge[1 - self.dqn.id]
            if opponentFlipTime:
                if self.dqn.lastFlipTime:
                    return np.array([self.currStep - opponentFlipTime, self.currStep - self.dqn.lastFlipTime])
                else:
                    return np.array([self.currStep - opponentFlipTime, self.currStep])
            return np.array([self.currStep, self.dqn.lastFlipTime])

        elif self.opp.strategy == 3: # exponential
            return np.array([self.dqn.lastFlipTime, self.steps - self.currStep])

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.
        :return:
        """

        globals.gGameFlips = {idx: [] for idx in range(globals.gNbAgents)}

        self.flips = []
        self.oppFlips = []
        self.currStep = -1  # reset step counter
        for agent in self.agents:
            agent.reset()

        self.dqn.setCurrentOwner()
        self.done = False  # reset end of game

        return self._get_state()  # get current state of game

    def train(self, eps_start=1.0, eps_end=0.01, eps_decay=0.995):
        """

        :param n_episodes:
        :param eps_start:
        :param eps_end:
        :param eps_decay:
        :return:
        """
        scores = []
        opp_scores = []
        av_scores = []
        oppAv_socres = []
        scores_window = deque(maxlen=100)
        eps = eps_start
        ep = -1

        while ep < 5000:
        #while not scores_window or np.mean(scores_window) < 78.0:
            ep += 1
            state = self.reset()
            for t in range(globals.gGameLength + 1):
                action = self.dqn.act(state, eps)
                next_state, reward, done, _ = self.step(action)
                self.dqn.step(state, action, reward, next_state, done)
                state = next_state
                if done:
                    break
            scores_window.append(self.dqn.score)
            scores.append(self.dqn.score)
            opp_scores.append(self.opp.score)
            eps = max(eps_end, eps_decay*eps)

            if ep % 100 == 0:
                av_scores.append(np.mean(scores_window))
                oppAv_socres.append(np.mean(opp_scores[-100:]))
                print('\rEpisode {}\tAverage Score: {:.2f}'.format(ep, np.mean(scores_window)))

                print('Adaptive agent score = {}, non-adaptive agent score = {}'.format(self.dqn.score, self.opp.score))
                print('Adaptive agent : {}'.format(self.flips))
                print('Opponent : {}\n'.format(self.oppFlips))

        print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}\tEpsilon: {}'.format(ep - 100, np.mean(scores_window), eps))
        torch.save(self.dqn.dqn_local.state_dict(), 'results/checkpoint.pth')
        return scores, av_scores, opp_scores, oppAv_socres


if __name__ == '__main__':
    setProperties(readProperties('../config/parameters/dqn.properties'))
    env = flipIt()
    print('State shape: ', env.state_size)
    print('Number of actions: ', env.action_size)
    print('\n')

    time = datetime.now()
    fname = 'plots/plot_' + str(time.year) + str(time.month) + str(time.day) + '-' + \
            str(time.hour) + 'h' + str(time.minute) + 'm' + str(time.second) + 's' + \
            str(time.microsecond) + 'us.png'

    # watch an untrained agent
    scores, av_scores, opp_scores, oppAv_socres = env.train()

    # plot scores
    fig = plt.figure(num=None, figsize=(12, 8), dpi=180, facecolor='w', edgecolor='k')
    plt.plot(np.arange(len(scores)), scores, color='#c1d1e0', linewidth=0.5, alpha=0.6)
    plt.plot(np.arange(len(av_scores))*100, av_scores, color='#7093b7', label='DQN Agent')
    plt.plot(np.arange(len(opp_scores)), opp_scores, color='#f998a5', linewidth=0.5, alpha=0.6)
    plt.plot(np.arange(len(oppAv_socres))*100, oppAv_socres, color='#ff0000', label='Opponent')
    plt.ylim(top=200)
    plt.ylabel('Score')
    plt.xlabel('Episode #')
    plt.legend(loc='best')
    plt.title('Game length = {}, flip cost = {}, flip reward = {}\n'.format(globals.gGameLength, globals.gFlipCost, globals.gFlipReward))
    plt.savefig(fname)
