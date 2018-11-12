#!/usr/bin/env python

from tkinter import *
from config import globals


class parameterFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=600, height=200)
        self.parent = master
        self.parameterFrame = None
        self.cost = None
        self.reward = None
        self.parameterChoice()

    def parameterChoice(self):
        """
        Parameter frame
        :return:
        """
        self.parameterFrame = LabelFrame(self, text="Game Parameters", padx=10, pady=10)

        # Cost box entry
        labelCost = Label(self.parameterFrame, text="Cost per flip : ", font=("", 12))
        self.cost = Entry(self.parameterFrame, textvariable=globals.gFlipCost, width=10)
        self.cost.insert(0, globals.gFlipCost)

        # Reward box entry
        labelReward = Label(self.parameterFrame, text="Reward per timestep : ", font=("", 12))
        self.reward = Entry(self.parameterFrame, textvariable=globals.gFlipReward, width=10)
        self.reward.insert(0, globals.gFlipReward)

        # Parameter frame
        labelCost.grid(row=0, column=0, sticky=W)
        self.cost.grid(row=0, column=1, sticky=W)
        labelReward.grid(row=1, column=0, sticky=W)
        self.reward.grid(row=1, column=1, sticky=W)

        self.parameterFrame.pack(side=LEFT, fill=BOTH, expand=1, padx=5, pady=5)