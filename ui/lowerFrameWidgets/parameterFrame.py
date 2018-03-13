# -*- coding: utf-8 -*-

from Tkinter import *


class parameterFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=600, height=200)
        self.parent = master
        self.parameterFrame = None
        self.cost = 0
        self.reward = 0
        self.parameterChoice()

    def parameterChoice(self):
        self.parameterFrame = LabelFrame(self, text="Game Parameters", padx=10, pady=10)
        labelCost = Label(self.parameterFrame, text="Cost per flip : ", font=("", 12))
        entryCost = Entry(self.parameterFrame, textvariable=self.cost, width=10)
        labelReward = Label(self.parameterFrame, text="Reward per timestep : ", font=("", 12))
        entryReward = Entry(self.parameterFrame, textvariable=self.reward, width=10)

        labelCost.grid(row=0, column=0, sticky=W)
        entryCost.grid(row=0, column=1, sticky=W)
        labelReward.grid(row=1, column=0, sticky=W)
        entryReward.grid(row=1, column=1, sticky=W)

        self.parameterFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)