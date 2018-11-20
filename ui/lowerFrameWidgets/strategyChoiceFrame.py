#!/usr/bin/env python

from tkinter import *
from config import globals

varInteractive = 5

class strategyChoiceFrame(Frame):
    def __init__(self, master, agents):
        Frame.__init__(self, master, width=600, height=200)
        self.parent = master
        self.agents = agents
        self.strategyChoiceFrame = None
        self.strategy0 = self.agents[0].strategy
        self.strategy1 = self.agents[1].strategy
        self.agents[0].strategy = IntVar()
        self.agents[1].strategy = IntVar()
        self.strategyChoice()

    def strategyChoice(self):
        # Variable initialization
        self.strategyChoiceFrame = LabelFrame(self, text="Agent Strategies", padx=10, pady=10)
        if globals.gInteractive:
            self.agents[0].strategy.set(varInteractive)
        else:
            self.agents[0].strategy.set(self.strategy0)
        self.agents[1].strategy.set(self.strategy1)

        # Widgets declaration
        labelS1 = Label(self.strategyChoiceFrame, text="Player 1", font=("", 12))
        labelS2 = Label(self.strategyChoiceFrame, text="Player 2", font=("", 12))

        radioStrategy1 = Radiobutton(self.strategyChoiceFrame, text="Periodic", variable=self.agents[0].strategy, value=0)
        radioStrategy11 = Radiobutton(self.strategyChoiceFrame, text="Uniform", variable=self.agents[0].strategy, value=1)
        radioStrategy12 = Radiobutton(self.strategyChoiceFrame, text="Delayed Uniform", variable=self.agents[0].strategy, value=2)
        radioStrategy13 = Radiobutton(self.strategyChoiceFrame, text="Exponential", variable=self.agents[0].strategy, value=3)
        radioStrategy14 = Radiobutton(self.strategyChoiceFrame, text="Delayed Exponential", variable=self.agents[0].strategy, value=4)
        radioInteractive = Radiobutton(self.strategyChoiceFrame, text="Interactive", variable=self.agents[0].strategy, value=varInteractive)

        radioStrategy2 = Radiobutton(self.strategyChoiceFrame, text="Periodic", variable=self.agents[1].strategy, value=0)
        radioStrategy21 = Radiobutton(self.strategyChoiceFrame, text="Uniform", variable=self.agents[1].strategy, value=1)
        radioStrategy22 = Radiobutton(self.strategyChoiceFrame, text="Delayed Uniform", variable=self.agents[1].strategy, value=2)
        radioStrategy23 = Radiobutton(self.strategyChoiceFrame, text="Exponential", variable=self.agents[1].strategy, value=3)
        radioStrategy24 = Radiobutton(self.strategyChoiceFrame, text="Delayed Exponential", variable=self.agents[1].strategy, value=4)

        # Widgets display
        labelS1.grid(row=0, column=0, columnspan=2, sticky=W)
        labelS2.grid(row=0, column=2, columnspan=2, sticky=W)
        radioStrategy1.grid(row=1, column=0, columnspan=2, sticky=W)
        radioStrategy11.grid(row=2, column=0, columnspan=2, sticky=W)
        radioStrategy12.grid(row=3, column=0, columnspan=2, sticky=W)
        radioStrategy13.grid(row=4, column=0, columnspan=2, sticky=W)
        radioStrategy14.grid(row=5, column=0, columnspan=2, sticky=W)
        radioInteractive.grid(row=6, column=0, columnspan=2, sticky=W)

        radioStrategy2.grid(row=1, column=2, columnspan=2, sticky=W)
        radioStrategy21.grid(row=2, column=2, columnspan=2, sticky=W)
        radioStrategy22.grid(row=3, column=2, columnspan=2, sticky=W)
        radioStrategy23.grid(row=4, column=2, columnspan=2, sticky=W)
        radioStrategy24.grid(row=5, column=2, columnspan=2, sticky=W)

        self.strategyChoiceFrame.pack(side=LEFT, fill=Y, padx=10, pady=10)