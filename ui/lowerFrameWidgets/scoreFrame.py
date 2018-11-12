#!/usr/bin/env python

from tkinter import *


class scoreFrame(Frame):
    def __init__(self, master, agents):
        Frame.__init__(self, master, width=600, height=200)
        self.parent = master
        self.agents = agents
        self.scoreFrame = None
        self.labelScoreP1 = None
        self.labelScoreP2 = None
        self.displayScore()

    def displayScore(self):
        # Variable initialization
        self.scoreFrame = LabelFrame(self, text="Current Score", padx=10, pady=10)

        # Widgets declaration
        self.labelScoreP1 = Label(self.scoreFrame, text="Player 1 : " + str("{0:.2f}".format(self.agents[0].score)),\
                                  width=15, anchor=W, font=("", 12))
        self.labelScoreP2 = Label(self.scoreFrame, text="Player 2 : " + str("{0:.2f}".format(self.agents[1].score)),\
                                  width=15, anchor=W, font=("", 12))

        # Widgets display
        self.labelScoreP1.grid(row=0, column=0, sticky=W)
        self.labelScoreP2.grid(row=1, column=0, sticky=W)

        self.scoreFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)

    def updateDisplayScore(self):
        self.labelScoreP1.config(text="Player 1 : " + str("{0:.2f}".format(self.agents[0].score)))
        self.labelScoreP2.config(text="Player 2 : " + str("{0:.2f}".format(self.agents[1].score)))