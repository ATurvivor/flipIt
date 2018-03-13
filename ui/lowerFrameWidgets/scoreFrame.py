# -*- coding: utf-8 -*-

from Tkinter import *


class scoreFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=600, height=200)
        self.parent = master
        self.scoreFrame = None
        self.scoreP1 = IntVar()
        self.scoreP2 = IntVar()
        self.labelScoreP1 = None
        self.labelScoreP2 = None
        self.displayScore()

    def displayScore(self):
        # Variable initialization
        self.scoreFrame = LabelFrame(self, text="Current Score", padx=10, pady=10)
        self.scoreP1.set(0)
        self.scoreP2.set(0)

        # Widgets declaration
        self.labelScoreP1 = Label(self.scoreFrame, text="Player 1 : " + str(self.scoreP1.get()), font=("", 12))
        self.labelScoreP2 = Label(self.scoreFrame, text="Player 2 : " + str(self.scoreP1.get()), font=("", 12))

        # Widgets display
        self.labelScoreP1.grid(row=0, column=0, sticky=W)
        self.labelScoreP2.grid(row=1, column=0, sticky=W)

        self.scoreFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)

    def updateScore(self):
        self.labelScoreP1.config(text="Player 1 : " + str(self.scoreP1.get()))
        self.labelScoreP2.config(text="Player 2 : " + str(self.scoreP2.get()))