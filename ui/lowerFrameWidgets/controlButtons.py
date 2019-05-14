#!/usr/bin/env python

from tkinter import *


from endGame import *
from config.log import initLog, writeLog

import numpy as np

varInteractive = 6

class controlButtons(Frame):
    def __init__(self, main, master, agents):
        Frame.__init__(self, master)
        self.main = main
        self.parent = master
        self.agents = agents
        self.controlButtonsFrame = None
        self.mode = 0 # 0 : game restarted, 1 : game started, 2 : game stopped
        self.startButton = None
        self.flipButton = None
        self._job = None
        self.displayButtons()

    def displayButtons(self):
        # Variable initialization
        self.controlButtonsFrame = LabelFrame(self, text="Control Buttons", padx=10, pady=10)

        # add play button
        self.startButton = Button(self.controlButtonsFrame, text="Play", command=self.play, width=8)
        self.startButton.grid(row=0, column=0, sticky=W)

        # add flip button
        self.flipButton = Button(self.controlButtonsFrame, text="Flip", command=self.flip, width=8)
        self.flipButton.grid(row=1, column=0, sticky=W)

        self.controlButtonsFrame.pack(side=LEFT, fill=Y, padx=10, pady=10)

    def updateMode(self):
        """
        Start, stop or restart game
        :return:
        """
        self.mode = (self.mode + 1) % 3 # update mode

        if self.mode == 1:
            self.start()
        elif self.mode == 2:
            self.stop()
        else:
            self.restart()

    def updateParameters(self):
        """

        :return:
        """
        globals.gLogFileName = initLog() # initialise log file name
        globals.gIteration = 0.0 # start iteration count
        globals.gEndGame = False
        globals.gCurrentOwner = self.agents[globals.gCurrentOwnerId]

        for agent in self.agents:
            agent.cost = self.parent.getCost()
            agent.reward = self.parent.getReward()

        if self.parent.getTimeType(): # finite
            globals.gLastIteration = globals.gGameLength
        elif self.parent.getGameType(): # infinite and continuous
            globals.gLastIteration = np.random.exponential(scale=1.0 / self.parent.getTimeType()[1])
        else: # infinite and discrete
            globals.gLastIteration = np.random.geometric(p=self.parent.getTimeType()[1])

        if self.agents[0].strategy.get() == varInteractive: # interactive mode
            globals.gInteractive = True
        else:
            globals.gInteractive = False

    def play(self):
        """
        Play game button
        :return:
        """
        if self.mode == 0:
            self.updateParameters()

            # update button states
            if globals.gInteractive:  # interactive
                self.flipButton.config(state="active")
            else:
                self.flipButton.config(state="disabled")

        self.updateMode()

    def start(self):
        """
        Start game button
        :return:
        """
        self.startButton.config(text="Stop")

        if globals.gDebug:
            print('Writing log in ' + str(globals.gLogFileName) + '\n')

        self._job = self.after(50, self.run)

    def stop(self):
        """
        Stop game button
        :return:
        """
        self.startButton.config(text="Restart")

        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None

        self.main.upperFrame.showFlips()

        if globals.gIteration < globals.gGameLength:
            globals.gCurrentOwner.addReward()

        self.updateDisplayScore()
        endGame(self.agents)

    def restart(self):
        """
        Restart game button
        :return:
        """
        self.startButton.config(text="Start")
        resetGame(self.agents)
        self.main.resetMainWindow()

    def flip(self):
        """
        Flip button
        :return:
        """
        self.agents[0].flip = True
        self.agents[0].flipTime = globals.gIteration
        self.main.upperFrame.addFlip(self.agents[0])  # flip
        self.main.upperFrame.showFlips()  # show previous flips

    def updateDisplayScore(self):
        """
        Updates display of scores
        :return:
        """
        self.parent.scoreFrame.updateDisplayScore()

    def generateRandomSeeds(self):
        """
        Generates random seeds for each agent
        :param agents: list of agents
        :return:
        """
        globals.gRandomSeeds = {agent.id:np.random.uniform(0, 1.0) for agent in self.agents}

    def run(self):
        """
        Run game
        :param agents:
        :param environment:
        :return:
        """
        if not globals.gEndGame:
            if globals.gDebug:
                print('\nCurrent iteration : ' + str(globals.gIteration))

            self.main.upperFrame.displayRun()

            writeLog(globals.gLogFileName, globals.gIteration, self.agents) # log data
            self.generateRandomSeeds()

            if self.decisionProcess(): # game ended
                self.updateMode()

        self._job = self.after(50, self.run)

    def decisionProcess(self):
        """
        Flip for each agent
        :param agents: list of agents
        :return: boolean, whether game ends
        """
        flipped = {}
        for agent in self.agents:
            if not globals.gInteractive or (globals.gInteractive and agent.id != 0): # any agent that is not human
                agent.flipDecision(continuous=0)
            flipped[agent] = agent.flip
        globals.gIteration += 1

        if globals.gDebug:
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
            flippedAgents = [agent for agent in flipped.keys() if flipped[agent]]
            for agent in flippedAgents:
                globals.gGameFlips[agent.id].append(globals.gIteration)

            for agent in flippedAgents:
                agent.updateKnowledge()
                agent.addPenalty()

            # choose new owner at random
            agentOrder = np.random.permutation(flippedAgents)
            globals.gCurrentOwner = agentOrder[-1]
            if globals.gDebug:
                print('New owner : ' + str(globals.gCurrentOwner.id))

            # add flip on board
            if not globals.gInteractive or (globals.gInteractive and globals.gCurrentOwner.id != 0):
                self.main.upperFrame.addFlip(globals.gCurrentOwner)

            # update score display
            if not globals.gInteractive or (globals.gInteractive and globals.gCurrentOwner.id == 0):
                self.updateDisplayScore()

        # check if end of game
        if globals.gIteration >= globals.gLastIteration:
            globals.gCurrentOwner.addReward()
            return True

        return False

