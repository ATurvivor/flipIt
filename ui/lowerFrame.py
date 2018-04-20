#!/usr/bin/env python

from Tkinter import *

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
    def __init__(self, master):
        Frame.__init__(self, master, width=600, height=200)
        self.parent = master # give direct access to mainWindow
        # Frames
        self.strategyChoiceFrame = strategyChoiceFrame(self, master)
        self.gameTypeFrame = gameTypeFrame(self, master)
        self.timeFrame = timeFrame(self, master)
        self.parameterFrame = parameterFrame(self, master)
        self.scoreFrame = scoreFrame(self, master)
        self.controlButtonsFrame = controlButtons(self, master)
        self.addWidgets()

    def addWidgets(self):
        self.strategyChoiceFrame.grid(row=0, column=0, columnspan=2, sticky=W+E+S+N)
        self.scoreFrame.grid(row=0, column=2, sticky=W+E+S+N)
        self.controlButtonsFrame.grid(row=0, column=3, sticky=W+E+S+N)
        self.gameTypeFrame.grid(row=1, column=0, sticky=W+E+S+N)
        self.timeFrame.grid(row=1, column=1, sticky=W+E+S+N)
        self.parameterFrame.grid(row=1, column=2, columnspan=2, sticky=W+E+S+N)
