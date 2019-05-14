# path
import sys
from os import getcwd

sys.path.append(getcwd())


import numpy as np
from gym import Env, spaces

from agents.agent import Agent
from older_versions.dqnAgent import dqnAgent

from config.properties import readProperties, setProperties
from config import globals

EPISODES = 600
BATCH_SIZE = 32

class flipItEnv(Env):
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
        self.dqn = dqnAgent(action_size=self.action_size, state_size=self.state_size) # adaptive agent
        if self.dqn.strategy != -1:  # check if non-adaptive
            raise Exception('Agent 0 should be an adaptive agent (strategy -1).')
        self.dqn.setCurrentOwner()  # initial owner
        self.opp = Agent(strategy=0, strategyParam=0.05)

        self.agents = [self.dqn, self.opp]
        
        # store what the agent tried
        self.currEpisode = -1
        self.actionEpisodeMemory = []

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
            if agent.strategy == -1: # adaptive strategy : don't flip (0) or flip (1)
                flipped[agent] = action
                if action:
                    agent.lastFlipTime = self.currStep
                    self.flips.append(self.currStep)
            else:
                globals.gIteration = self.currStep
                agent.flipDecision() # run corresponding strategy
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

            if len(flippedAgents) == 1:
                flippedAgents[0].setCurrentOwner()
            else:
                # give priority to DQN agent if both flipped
                self.dqn.setCurrentOwner()
                # self.oppAgent.setCurrentOwner()

        # end of game
        if self.currStep >= self.steps:
            self.done = True
            print('Episode {} : adaptive agent score = {}, non-adaptive agent score = {}'.format(self.currEpisode, self.agents[0].score, self.agents[1].score))
            print('Adaptive agent : {}'.format(self.flips))
            print('Opponent : {}'.format(self.oppFlips))

        return actionReward

    def _get_state(self):
        """
        Get observation (time since last opponent flip)
        :return:
        """
        # opponentFlipTime = self.dqn.knowledge[1 - self.dqn.id]
        # if opponentFlipTime:
        #     if self.dqn.lastFlipTime:
        #         return [self.currStep - opponentFlipTime, self.currStep - self.dqn.lastFlipTime]
        #     else:
        #         return [self.currStep - opponentFlipTime, self.currStep]
        # return [self.currStep, self.dqn.lastFlipTime]

        return [self.dqn.lastFlipTime, self.steps - self.currStep]

        # opponentFlipTime = self.dqn.knowledge[1 - self.dqn.id]
        # return [opponentFlipTime, self.currStep, self.dqn.isCurrentOwner()]

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.

        Returns
        -------
        observation (object): the initial observation of the space.
        """
        globals.gGameFlips = {idx: [] for idx in range(globals.gNbAgents)}

        self.flips = []
        self.oppFlips = []
        self.currStep = -1  # reset step counter
        for agent in self.agents:
            agent.reset()

        self.dqn.setCurrentOwner()
        self.done = False  # reset end of game
        self.actionEpisodeMemory.append([])

        self.currEpisode += 1  # increase episode number

        return self._get_state()  # get current state of game

    def learn(self):
        for e in range(EPISODES):
            state = self.reset()
            state = np.reshape(state, [1, self.state_size])
            for time in range(globals.gGameLength + 1):
                # env.render()
                action = self.dqn.act(state)
                next_state, reward, done, _ = env.step(action)
                next_state = np.reshape(next_state, [1, self.state_size])
                self.dqn.remember(state, action, reward, next_state, done)
                state = next_state
                if done:
                    break
                if len(self.dqn.memory) > BATCH_SIZE:
                    self.dqn.replay(BATCH_SIZE)

if __name__ == '__main__':
    setProperties(readProperties('../config/parameters/dqn.properties'))

    env = flipItEnv()
    env.learn()