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
        self.strategyChoiceFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        self.gameTypeFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        self.timeFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        self.parameterFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        self.scoreFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        self.controlButtonsFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)