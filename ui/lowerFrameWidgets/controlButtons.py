# -*- coding: utf-8 -*-

from Tkinter import *

class controlButtons(Frame):
    """

    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.controlButtonsFrame = None
        self.displayButtons()

    def displayButtons(self):
        # Variable initialization
        self.controlButtonsFrame = LabelFrame(self, text="Control Buttons", padx=10, pady=10)

        # add start button
        startButton = Button(self.controlButtonsFrame, text="Play", command=self.start)
        startButton.grid(row=0, column=0, sticky=W)

        # add flip button
        flipButton = Button(self.controlButtonsFrame, text="Flip", command=self.flip)
        flipButton.grid(row=1, column=0, sticky=W)

        self.controlButtonsFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)

    def start(self):
        self.updateScore()
        self.updateBoard()

    def flip(self):
        return 0

    def updateScore(self):
        self.parent.scoreFrame.scoreP1.set(self.parent.scoreFrame.scoreP1.get()+1) # modify
        # Update scores for P1 and P2 wrt. flip it rules
        self.parent.scoreFrame.updateScore()

    def updateBoard(self):
        # update Board
        return 0