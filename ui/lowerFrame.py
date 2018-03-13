# -*- coding: utf-8 -*-

from Tkinter import *

from ui.lowerFrameWidgets.strategyChoiceFrame import strategyChoiceFrame
from ui.lowerFrameWidgets.gameTypeFrame import gameTypeFrame
from ui.lowerFrameWidgets.parameterFrame import parameterFrame
from ui.lowerFrameWidgets.scoreFrame import scoreFrame
from ui.lowerFrameWidgets.controlButtons import controlButtons


class lowerFrame(Frame):
    """
    Lower frame of UI
    """
    def __init__(self, master):
        Frame.__init__(self, master, width=600, height=200)
        self.parent = master
        # Frames
        self.strategyChoiceFrame = strategyChoiceFrame(self)
        self.gameTypeFrame = gameTypeFrame(self)
        self.parameterFrame = parameterFrame(self)
        self.scoreFrame = scoreFrame(self)
        self.controlButtonsFrame = controlButtons(self)
        self.addWidgets()

    def addWidgets(self):
        self.strategyChoiceFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        self.gameTypeFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        self.parameterFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        self.scoreFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
        self.controlButtonsFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)