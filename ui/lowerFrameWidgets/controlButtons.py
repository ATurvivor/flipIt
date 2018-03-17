# -*- coding: utf-8 -*-

from Tkinter import *

from endGame import *
from datetime import datetime

class controlButtons(Frame):
    """
    Start and Flip buttons
    """
    def __init__(self, master, root):
        Frame.__init__(self, master)
        self.root = root
        self.parent = master
        self._job = None
        self.mode = 0 # 0 : game over, 1 : game started
        self.controlButtonsFrame = None
        self.startButton = None
        self.displayButtons()

    def displayButtons(self):
        # Variable initialization
        self.controlButtonsFrame = LabelFrame(self, text="Control Buttons", padx=10, pady=10)

        # add start button
        self.startButton = Button(self.controlButtonsFrame, text="Play", command=self.start, width=8)
        self.startButton.grid(row=0, column=0, sticky=W)

        # add flip button
        flipButton = Button(self.controlButtonsFrame, text="Flip", command=self.flip, width=8)
        flipButton.grid(row=1, column=0, sticky=W)

        self.controlButtonsFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)

    def start(self):
        self.updateBoard()
        self.updateScore()

    def stop(self):
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None

    def flip(self):
        if self.mode:
            self.root.agents[0].score += 1
            self.updateScore()

    def updateBoard(self):
        """
        Start or end game
        :return:
        """
        self.mode = (self.mode + 1) % 2 # update mode
        if self.mode:
            globals.gIteration = 0 # start iteration count

            # data log file name
            time = datetime.now()
            globals.gLogFileName = 'logs/datalog_' + str(time.year) + str(time.month) + str(time.day) + '-' +\
               str(time.hour) + 'h' + str(time.minute) + 'm' + str(time.second) + 's' + str(time.microsecond) + 'us.txt'

            globals.gEndGame = False
            self.root.upperFrame.running = True
            self.startButton.config(text="Reset")
            self._job = self.after(500, self.run, globals.gLogFileName, self.root.agents, self.root)

        else:
            self.root.upperFrame.running = False
            self.startButton.config(text="Start")
            self.stop()
            # TODO : fix end critera : resetGame if finite, verifyEndGame if infinite
            resetGame(self.root.agents, self.root)


    def updateScore(self):
        """
        Updates display of scores
        :return:
        """
        self.parent.scoreFrame.updateDisplayScore()

    def run(self, fileName, agents, environment=None):
        """
        Run game
        :param fileName:
        :param agents:
        :param environment:
        :return:
        """
        if not globals.gEndGame:
            # at each iteration
            if environment:
                environment.upperFrame.displayRun()

            log.writeLog(fileName, globals.gIteration, agents) # log data
            # calculateRandomSeeds()
            # decisionProcess()
            # update()
            # verifyEndGame()

            globals.gIteration += 1
            print(globals.gIteration)

        self._job = self.after(500, self.run, fileName, agents, environment)