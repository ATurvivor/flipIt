# -*- coding: utf-8 -*-

from Tkinter import *
from endGame import *
from run import *

class controlButtons(Frame):
    """
    Start and Flip buttons
    """
    def __init__(self, master, root):
        Frame.__init__(self, master)
        self.root = root
        self.parent = master
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
        self.updateButton()
        self.updateScore()
        self.updateBoard()

    def flip(self):
        if self.mode:
            self.root.agents[0].score += 1
            self.updateScore()

    def updateButton(self):
        """
        Updates 'start' display and resets game if necessary
        :return:
        """
        self.mode = (self.mode + 1) % 2 # update mode
        if self.mode:
            # data log file name
            time = datetime.now()
            globals.gLogFileName = 'log/datalog_' + str(time.year) + str(time.month) + str(time.day) + '-' +\
               str(time.hour) + 'h' + str(time.minute) + 'm' + str(time.second) + 's' + str(time.microsecond) + 'us.txt'

            # TODO : fix run display with environment
            self.root.upperFrame.running = True
            self.startButton.config(text="Reset")
            self.after(50,self.root.upperFrame.displayRun())

            run(globals.gLogFileName, self.root.agents, self.root)
        else:
            self.root.upperFrame.running = False
            self.startButton.config(text="Start")
            resetGame(self.root.agents, self.root)

    def updateScore(self):
        """
        Updates display of scores
        :return:
        """
        self.parent.scoreFrame.updateDisplayScore()
        #self.parent.scoreFrame.labelScoreP1.config(text="Player 1 : " + str(self.root.a1.score))
        #self.parent.scoreFrame.labelScoreP2.config(text="Player 2 : " + str(self.root.a2.score))

    def updateBoard(self):
        """
        Updates board
        :return:
        """
        return 0