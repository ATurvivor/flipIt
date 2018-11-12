#!/usr/bin/env python

from tkinter import *
from config import globals


class timeFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=600, height=200)
        self.parent = master
        self.timeVariableFrame = None
        self.time = IntVar()
        self.probability = StringVar() # TODO complete
        self.timeVariableChoice()

    def timeVariableChoice(self):
        # Variable initialization
        self.timeVariableFrame = LabelFrame(self, text="Time Variable", padx=10, pady=10)
        self.time.set(globals.gFiniteTime)
        self.probability.set(globals.gEndGameProbability)

        # Widgets declaration
        labelP = Label(self.timeVariableFrame, text="Probability : ", font=("", 12))
        radioInfinite = Radiobutton(self.timeVariableFrame, text="Infinite", variable=self.time, value=0)
        radioFinite = Radiobutton(self.timeVariableFrame, text="Finite", variable=self.time, value=1)
        entryProbability = Entry(self.timeVariableFrame, textvariable=self.probability, width=6)

        # Widgets display
        radioInfinite.grid(row=0, column=0, columnspan=2, sticky=W)
        labelP.grid(row=1, column=0, sticky=W)
        entryProbability.grid(row=1, column=1, columnspan=2, sticky=W)
        radioFinite.grid(row=2, column=0, columnspan=2, sticky=W)

        self.timeVariableFrame.pack(side=LEFT, fill=BOTH, expand=1, padx=5, pady=5)