#!/usr/bin/env python

from Tkinter import *

from config import globals


class parameterFrame(Frame):
    def __init__(self, master, root):
        Frame.__init__(self, master, width=600, height=200)
        self.root = root # mainWindow frame
        self.parent = master
        self.parameterFrame = None
        self.entryCost = None
        self.entryReward = None
        self.cost = globals.gFlipCost
        self.reward = globals.gFlipReward
        self.parameterChoice()

    def parameterChoice(self):
        """
        Parameter frame
        :return:
        """
        self.parameterFrame = LabelFrame(self, text="Game Parameters", padx=10, pady=10)

        # Cost box entry
        labelCost = Label(self.parameterFrame, text="Cost per flip : ", font=("", 12))
        self.entryCost = Entry(self.parameterFrame, textvariable=self.cost, width=10)
        self.entryCost.insert(0, self.cost)

        # Reward box entry
        labelReward = Label(self.parameterFrame, text="Reward per timestep : ", font=("", 12))
        self.entryReward = Entry(self.parameterFrame, textvariable=self.reward, width=10)
        self.entryReward.insert(0, self.reward)

        # Parameter frame
        labelCost.grid(row=0, column=0, sticky=W)
        self.entryCost.grid(row=0, column=1, sticky=W)
        labelReward.grid(row=1, column=0, sticky=W)
        self.entryReward.grid(row=1, column=1, sticky=W)

        self.parameterFrame.pack(side=LEFT, fill=BOTH, expand=1, padx=5, pady=5)

    def getCost(self):
        """
        Returns cost
        :return:
        """
        return eval(self.entryCost.get())

    def getReward(self):
        """
        Returns reward
        :return:
        """
        return eval(self.entryReward.get())