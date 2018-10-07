#!/usr/bin/env python

import numpy as np

from strategies.basics import *

class Agent:
    def __init__(self, strategy=0, strategyParam=(.01)):
        self.id = globals.gAgentStartId
        self.score = 0.0
        self.cost = globals.gFlipCost
        self.reward = globals.gFlipReward
        self.strategy = strategy # strategy
        self.strategyParam = strategyParam
        self.flip = False
        self.flipTime = 10.0
        self.lastFlipTime = 0
        #self.history = [] # list history of flip times
        self.perspectiveHistory = np.zeros(globals.gNbAgents) #history lengths from this players perspective
        self.updateAgentIds()

    def updateAgentIds(self):
        globals.gAgentStartId += 1

    def flipDecision(self, gameType):
        """
        Runs agent's strategy and updates its score
        :param gameType: continuous or discrete
        :return:
        """
        strategies = {0 : randomDecayed, 1 : periodic, 2 : delayedRandomDecayed}
        if globals.gEnvironment:
            return strategies[self.strategy.get()](self, gameType)
        return strategies[self.strategy](self, gameType)
        #return run_strategy(self, gameType)

    def addPenalty(self):
        """
        Add flip cost
        :return:
        """
        self.score -= self.cost

        if globals.gDebug:
            print('Agent ' + str(self.id) + ' flipped. Adding penalty. New score is ' + str(self.score) + '.')

    def addReward(self):
        """
        Update score of previous owner of resource
        :return:
        """
        self.score += (globals.gIteration - self.lastFlipTime) * self.reward

        if globals.gDebug:
            print('Agent ' + str(self.id) + ' has score ' + str(self.score) + ' after reward.')

    def updateTimeVector(self):
        # TODO update time vectors
        return 0

    def updateHistory(self):
        # TODO update own time vectors, perspective time vectors
        globals.gGameFlips[self.id].append(globals.gIteration)
        for i in range(globals.gNbAgents):
            self.perspectiveHistory[i]=len(globals.gGameFlips[i])
