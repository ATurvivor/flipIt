#!/usr/bin/env python

from tkinter import *
from ui.lowerFrame import lowerFrame
from ui.upperFrame import upperFrame

class MainWindow(Frame):
    """
    Frame containing all elements
    """
    def __init__(self, master, agents):
        Frame.__init__(self, master)
        self.parent = master
        self.agents = agents
        self.upperFrame = upperFrame(self)
        self.lowerFrame = lowerFrame(self, agents)
        self.packElements()

    def packElements(self):
        self.upperFrame.pack(side=TOP, padx=10, pady=10)
        self.lowerFrame.pack(side=BOTTOM, padx=10, pady=(10,50))

    def resetMainWindow(self):
        """
        Reset main window
        :return:
        """
        self.lowerFrame.scoreFrame.updateDisplayScore()
        self.upperFrame.resetBoard()
