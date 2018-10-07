#!/usr/bin/env python

from Tkinter import *

from endGame import *
from run import run_environment
from config.log import initLogFileName, writeLog

import numpy as np

class controlButtons(Frame):
    """
    Start and Flip buttons
    """
    def __init__(self, master, root):
        Frame.__init__(self, master)
        self.root = root
        self.parent = master
        self.controlButtonsFrame = None
        self.mode = 0 # 0 : game over, 1 : game started, 2 : game stopped
        self._job = None
        self.startButton = None
        self.flipButton = None
        self.displayButtons()

    def displayButtons(self):
        # Variable initialization
        self.controlButtonsFrame = LabelFrame(self, text="Control Buttons", padx=10, pady=10)

        # add start button
        self.startButton = Button(self.controlButtonsFrame, text="Play", command=self.play, width=8)
        self.startButton.grid(row=0, column=0, sticky=W)

        # add flip button
        self.flipButton = Button(self.controlButtonsFrame, text="Flip", command=self.flip, width=8)
        self.flipButton.grid(row=1, column=0, sticky=W)

        self.controlButtonsFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)

    def initParameters(self):
        globals.gLogFileName = initLogFileName() # initialise log file name
        globals.gIteration = 0.0 # start iteration count
        globals.gEndGame = False

        for ag in self.root.agents:
            ag.cost = self.getCost()
            ag.reward = self.getReward()

        if self.getTimeType(): # finite
            globals.gGameEnd = globals.gLastIteration
        elif self.getGameType() == 0: # infinite and continuous
            globals.gGameEnd = np.random.exponential(scale=1.0 / self.getTimeType()[1])
        else: # infinite and discrete
            globals.gGameEnd = np.random.geometric(p=self.getTimeType()[1])

        if self.getAgent0().strategy.get() == 3: # interactive
            globals.gInteractive = True
        else:
            globals.gInteractive = False

    def updateButtonStates(self):
        if globals.gInteractive:  # interactive
            self.flipButton.config(state="active")
        else:
            self.flipButton.config(state="disabled")

    def play(self):
        """
        Play game button
        :return:
        """
        self.initParameters()
        if self.mode == 0:
            self.updateButtonStates()

        self.updateBoard()
        self.updateScore()

    def start(self):
        """
        Start game button
        :return:
        """
        self.initParameters()

        if globals.gDebug:
            print('Writing log in ' + str(globals.gLogFileName) + '\n')

        self.root.upperFrame.running = True
        self.startButton.config(text="Stop")
        self._job = self.after(50, self.run, self.root.agents)

    def stop(self):
        """
        Stop game button
        :return:
        """
        self.root.upperFrame.running = False
        self.startButton.config(text="Restart")

        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None

        globals.gCurrentOwner.addReward()
        self.root.upperFrame.showFlips()
        self.updateScore()
        endGame(self.root.agents)


    def restart(self):
        """
        Restart game button
        :return:
        """
        self.startButton.config(text="Start")
        resetGame(self.root.agents)
        self.root.resetMainWindow()

    def flip(self):
        """
        Flip button
        :return:
        """
        self.getAgent0().flip = True
        self.getAgent0().flipTime = globals.gIteration  # TODO fix continuous value
        self.root.upperFrame.addFlip(self.getAgent0())  # flip
        self.root.upperFrame.showFlips()  # show previous flips
        self.updateScore()

    def updateBoard(self):
        """
        Start, stop or restart game
        :return:
        """
        self.mode = (self.mode + 1) % 3 # update mode

        if self.mode == 1: self.start()
        elif self.mode == 2: self.stop()
        else: self.restart()

    def updateScore(self):
        """
        Updates display of scores
        :return:
        """
        self.parent.scoreFrame.updateDisplayScore()

    def run(self, agents):
        """
        Run game
        :param agents:
        :param environment:
        :return:
        """
        run_environment(self, agents)

    def getCost(self):
        return eval(self.parent.parameterFrame.entryCost.get())

    def getReward(self):
        return eval(self.parent.parameterFrame.entryReward.get())

    def getGameType(self):
        return self.parent.gameTypeFrame.type

    def getTimeType(self):
        return self.parent.timeFrame.time, eval(self.parent.timeFrame.probability.get())

    def getAgent0(self):
        return self.root.agents[0]
