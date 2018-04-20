#!/usr/bin/env python

from Tkinter import *

from endGame import *
from run import generateRandomSeeds, decisionProcess
from config.log import writeLog
from config.init import initGame


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

    def play(self):
        """
        Play game
        :return:
        """

        if self.mode == 0:
            self.updateButtonStates()
            initGame(self.parent)

        self.updateBoard()
        self.updateScore()

    def start(self):
        """
        Start game
        :return:
        """
        globals.gIteration = 0 # start iteration count

        if globals.gDebug:
            print('Writing log in ' + str(globals.gLogFileName) + '\n')

        globals.gEndGame = False

        self.root.upperFrame.running = True
        self.startButton.config(text="Stop")
        self._job = self.after(50, self.run, self.root.agents)

    def stop(self):
        """
        Stop game
        :return:
        """
        self.root.upperFrame.running = False
        self.startButton.config(text="Restart")

        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None

        self.root.upperFrame.showFlips()
        globals.gCurrentOwner.addReward()
        self.updateScore()
        endGame(self.root.agents)


    def restart(self):
        """
        Restart game
        :return:
        """
        self.startButton.config(text="Start")
        resetGame(self.root.agents)
        self.root.resetMainWindow()

    def flip(self):
        """
        Flip
        :return:
        """
        self.root.agents[0].flip = True
        self.root.agents[0].flipTime = globals.gIteration  # TODO fix continuous value
        self.root.upperFrame.addFlip(self.root.agents[0])  # flip
        self.root.upperFrame.showFlips()  # show previous flips
        self.updateScore()

    def updateButtonStates(self):
        if self.root.agents[0].strategy.get() != 3:  # not interactive
            self.flipButton.config(state="disabled")
        else:
            self.flipButton.config(state="active")

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
        if not globals.gEndGame:
            # at each iteration
            if globals.gDebug:
                print('\nCurrent iteration : ' + str(globals.gIteration))

            self.root.upperFrame.displayRun()

            writeLog(globals.gLogFileName, globals.gIteration, agents) # log data
            generateRandomSeeds(agents)

            if decisionProcess(agents, self.parent):
                self.updateBoard()

            if not globals.gInteractive:
                self.updateScore()

        self._job = self.after(50, self.run, agents)

