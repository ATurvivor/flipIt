# -*- coding: utf-8 -*-

from Tkinter import *


class scoreFrame(Frame):
    def __init__(self, master, root):
        Frame.__init__(self, master, width=600, height=200)
        self.root = root # mainWindow Frame
        self.parent = master
        self.scoreFrame = None
        self.labelScoreP1 = None
        self.labelScoreP2 = None
        self.displayScore()

    def displayScore(self):
        # Variable initialization
        self.scoreFrame = LabelFrame(self, text="Current Score", padx=10, pady=10)

        # Widgets declaration
        self.labelScoreP1 = Label(self.scoreFrame, text="Player 1 : " + str(self.root.agents[0].score), font=("", 12))
        self.labelScoreP2 = Label(self.scoreFrame, text="Player 2 : " + str(self.root.agents[1].score), font=("", 12))

        # Widgets display
        self.labelScoreP1.grid(row=0, column=0, sticky=W)
        self.labelScoreP2.grid(row=1, column=0, sticky=W)

        self.scoreFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)

    def updateDisplayScore(self):
        self.labelScoreP1.config(text="Player 1 : " + str(self.root.agents[0].score))
        self.labelScoreP2.config(text="Player 2 : " + str(self.root.agents[1].score))