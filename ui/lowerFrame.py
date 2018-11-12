#!/usr/bin/env python

from tkinter import *

from ui.lowerFrameWidgets.strategyChoiceFrame import strategyChoiceFrame
from ui.lowerFrameWidgets.gameTypeFrame import gameTypeFrame
from ui.lowerFrameWidgets.timeFrame import timeFrame
from ui.lowerFrameWidgets.parameterFrame import parameterFrame
from ui.lowerFrameWidgets.scoreFrame import scoreFrame
from ui.lowerFrameWidgets.controlButtons import controlButtons


class lowerFrame(Frame):
    """
    Lower frame of UI
    """
    def __init__(self, master, agents):
        Frame.__init__(self, master, width=600, height=200)
        self.parent = master
        self.strategyChoiceFrame = strategyChoiceFrame(self, agents)
        self.gameTypeFrame = gameTypeFrame(self)
        self.timeFrame = timeFrame(self)
        self.parameterFrame = parameterFrame(self)
        self.scoreFrame = scoreFrame(self, agents)
        self.controlButtonsFrame = controlButtons(master, self, agents)
        self.addWidgets()

    def addWidgets(self):
        self.strategyChoiceFrame.grid(row=0, column=0, columnspan=2, sticky=W+E+S+N)
        self.scoreFrame.grid(row=0, column=2, sticky=W+E+S+N)
        self.controlButtonsFrame.grid(row=0, column=3, sticky=W+E+S+N)
        self.gameTypeFrame.grid(row=1, column=0, sticky=W+E+S+N)
        self.timeFrame.grid(row=1, column=1, sticky=W+E+S+N)
        self.parameterFrame.grid(row=1, column=2, columnspan=2, sticky=W+E+S+N)

    def getCost(self):
        """
        Return flip cost
        :return:
        """
        return eval(self.parameterFrame.cost.get())

    def getReward(self):
        """
        Return flip reward
        :return:
        """
        return eval(self.parameterFrame.reward.get())

    def getGameType(self):
        """
        Return game type (discrete, continuous)
        :return:
        """
        return self.gameTypeFrame.type.get()

    def getTimeType(self):
        """
        Return time type (infinite, finite)
        :return:
        """
        return self.timeFrame.time, eval(self.timeFrame.probability.get())

    def getAgent0(self):
        """

        :return:
        """
        return self.agents[0]

