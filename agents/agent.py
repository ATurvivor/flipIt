#!/usr/bin/env python

from ext import globals
import numpy as np

class Agent:
    def __init__(self, strategy=0):
        self.id = globals.gAgentId
        globals.gAgentId += 1
        self.score = 0
        self.cost = globals.gFlipCost
        self.reward = globals.gFlipReward
        self.strategy = strategy  # 0 : default random, 1 : adaptive, etc...
        self.flip = False
        self.lastFlipTime = 0

    def flipDecision(self):
        """
        Runs agent's strategy and updates its score
        :return:
        """
        # TODO : strategies (choose strategy)
        if np.random.uniform(0,1) < globals.gRandomSeeds[self.id]:
            self.flip = True
        #self.updateTimeVector()
        return self.flip

    def flipPenalty(self):
        """
        Add flip cost
        :return:
        """
        self.score -= globals.gFlipCost

        if globals.gDebug:
             print('Agent ' + str(self.id) + ' flipped. Adding penalty. New score is ' + str(self.score) + '.')

    def setStrategy(self, strategy):
        """

        :param strategy:
        :return:
        """
        return 0

    def updateScore(self):
        """
        Update score of previous owner of resource
        :return:
        """
        self.score += (globals.gIteration - self.lastFlipTime) * globals.gFlipReward
        if globals.gDebug:
            print('Agent ' + str(self.id) + ' has new score ' + str(self.score) + '.')

    def updateTimeVector(self):
        # TODO update time vectors
        return 0

    def updateHistory(self):
        # TODO update own time vectors, perspective time vectors
        return 0