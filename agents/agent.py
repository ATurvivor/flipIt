#!/usr/bin/env python

from strategies.basics import *


class Agent:
    def __init__(self, strategy=0, strategyParam=(.01), type=None):
        self.id = globals.gAgentStartId
        self.type = type # None, LM (last move) or FH (full history)
        self.score = 0.0
        self.cost = globals.gFlipCost
        self.reward = globals.gFlipReward
        self.strategy = strategy # strategy
        self.strategyParam = strategyParam
        self.flip = False
        self.flipTime = 10.0
        self.lastFlipTime = 0
        if self.type == 'LM':
            self.knowledge = {idx: None for idx in range(globals.gNbAgents)}  # list knowledge of flip times
        else:
            self.knowledge = {idx : [] for idx in range(globals.gNbAgents)} # list knowledge of flip times
        self.updateAgentIds()

    def updateAgentIds(self):
        globals.gAgentStartId += 1

    def setId(self, id):
        self.id = id

    def flipDecision(self, continuous=0):
        """
        Runs agent's strategy and updates its score
        :param continuous: continuous or discrete
        :return:
        """
        strategies = {0 : periodic, 1 : uniform, 2 : delayedUniform, 3 : exponential, 4 : delayedExponential, 5 : idle}
        if globals.gEnvironment:
            return strategies[self.strategy.get()](self, continuous)
        return strategies[self.strategy](self, continuous)

    def addPenalty(self):
        """
        Add flip cost
        :return:
        """
        self.score -= self.cost
        self.lastFlipTime = globals.gIteration
        self.flip = False

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

    def updateKnowledge(self):
        """
        Update agent's perspective depending on type (LM, FH)
        :return:
        """
        for idx in range(globals.gNbAgents):
            if self.type == 'LM': # last move
                try: # if opponent did not flip, this would return an error
                    if not self.knowledge[idx] or self.knowledge[idx] != globals.gGameFlips[idx][-1]:
                        self.knowledge[idx] = globals.gGameFlips[idx][-1] # only knows most recent flip
                        # keeps storing known recent moves
                        #self.knowledge[idx].append(globals.gGameFlips[idx][-1])
                except:
                    pass
            elif self.type == 'FH': # full history
                try:
                    self.knowledge[idx] = globals.gGameFlips[idx] # list of game flips for agent idx
                except:
                    pass

    def reset(self):
        """
        Resets agent parameters to default
        :return:
        """
        self.score = 0.0
        self.flip = False
        self.flipTime = 10.0
        self.lastFlipTime = 0
        if self.type == 'LM':
            self.knowledge = {idx: None for idx in range(globals.gNbAgents)}  # list knowledge of flip times
        else:
            self.knowledge = {idx: [] for idx in range(globals.gNbAgents)}  # list knowledge of flip times

    def setCurrentOwner(self):
        """
        Set agent as current owner of the resource
        :return: None
        """
        globals.gCurrentOwner = self

    def isCurrentOwner(self):
        """
        Returns True if agents is current owner of the resource
        :return: boolean
        """
        return self == globals.gCurrentOwner
