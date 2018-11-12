#!/usr/bin/env python

from tkinter import *
from config import globals

class strategyChoiceFrame(Frame):
    def __init__(self, master, agents):
        Frame.__init__(self, master, width=600, height=200)
        self.parent = master
        self.agents = agents
        self.strategyChoiceFrame = None
        self.agents[0].strategy = IntVar()
        self.agents[1].strategy = IntVar()
        self.strategyChoice()

    def strategyChoice(self):
        # Variable initialization
        self.strategyChoiceFrame = LabelFrame(self, text="Agent Strategies", padx=10, pady=10)
        if globals.gInteractive:
            self.agents[0].strategy.set(3)
        else:
            self.agents[0].strategy.set(0)
        self.agents[1].strategy.set(0)

        # Widgets declaration
        labelS1 = Label(self.strategyChoiceFrame, text="Player 1", font=("", 12))
        labelS2 = Label(self.strategyChoiceFrame, text="Player 2", font=("", 12))

        radioRandomDec1 = Radiobutton(self.strategyChoiceFrame, text="Random Decayed", variable=self.agents[0].strategy, value=0)
        radioPeriodic1 = Radiobutton(self.strategyChoiceFrame, text="Periodic", variable=self.agents[0].strategy, value=1)
        radioDelRandomDec1 = Radiobutton(self.strategyChoiceFrame, text="Delayed Random Decayed", variable=self.agents[0].strategy, value=2)
        radioInteractive = Radiobutton(self.strategyChoiceFrame, text="Interactive", variable=self.agents[0].strategy, value=3)
        radioRandomDec2 = Radiobutton(self.strategyChoiceFrame, text="Random Decayed", variable=self.agents[1].strategy, value=0)
        radioPeriodic2 = Radiobutton(self.strategyChoiceFrame, text="Periodic", variable=self.agents[1].strategy, value=1)
        radioDelRandomDec2 = Radiobutton(self.strategyChoiceFrame, text="Delayed Random Decayed", variable=self.agents[1].strategy, value=2)

        # Widgets display
        labelS1.grid(row=0, column=0, columnspan=2, sticky=W)
        labelS2.grid(row=0, column=2, columnspan=2, sticky=W)
        radioRandomDec1.grid(row=1, column=0, columnspan=2, sticky=W)
        radioPeriodic1.grid(row=2, column=0, columnspan=2, sticky=W)
        radioDelRandomDec1.grid(row=3, column=0, columnspan=2, sticky=W)
        radioInteractive.grid(row=5, column=0, columnspan=2, sticky=W)
        radioRandomDec2.grid(row=1, column=2, columnspan=2, sticky=W)
        radioPeriodic2.grid(row=2, column=2, columnspan=2, sticky=W)
        radioDelRandomDec2.grid(row=3, column=2, columnspan=2, sticky=W)

        self.strategyChoiceFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)