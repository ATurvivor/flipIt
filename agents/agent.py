#!/usr/bin/env python

from ext import globals
import numpy as np
from strategies import basics

class Agent:
    def __init__(self, strategy=0,strategyParam=(.05)):
        self.id = globals.gAgentStartId
        globals.gAgentStartId += 1
        self.score = 0
        self.cost = globals.gFlipCost
        self.reward = globals.gFlipReward
        self.strategyParam=strategyParam
        self.flip = False
        self.flipTime= 10.0
        self.lastFlipTime = 0
        self.history=[]
        # list history of flip times
        self.perspectiveHistory =np.zeros(globals.gNbAgents) #history lengths from this players perspective
        self.strategy=strategy #strategy



    def flipDecision(self):
        """
        Runs agent's strategy and updates its score
        :return:
        """
        # TODO : strategies (choose strategy)
        return basics.run_strategy(self)

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
        globals.gGameFlips[self.id].append(globals.gIteration)
        for i in range(globals.gNbAgents):
            self.perspectiveHistory[i]=len(globals.gGameFlips[i])
        return 0