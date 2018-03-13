# -*- coding: utf-8 -*-

from Tkinter import *
from ui.lowerFrame import lowerFrame
from ui.upperFrame import upperFrame

class MainWindow(Frame):
    """
    Frame containing all elements
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.upperFrame = upperFrame(self)
        self.lowerFrame = lowerFrame(self)
        self.packElements()

    def packElements(self):
        self.packUpperFrame()
        self.packLowerFrame()

    def packUpperFrame(self):
        if self.upperFrame:
            self.upperFrame.pack(side=TOP, padx=10, pady=10)

    def packLowerFrame(self):
        if self.lowerFrame:
            self.lowerFrame.pack(side=BOTTOM, padx=10, pady=10)

    def setUpperFrame(self, frame):
        """
        Change the upperFrame
        :param frame: widget that will replace the old one
        """
        if self.upperFrame:
            self.upperFrame.destroy()
        self.upperFrame = frame
        self.packUpperFrame()

    def setLowerFrame(self, frame):
        """
        Change the lowerFrameWidgets
        :param frame: widget that will replace the old one
        """
        if self.lowerFrame:
            self.lowerFrame.destroy()
        self.lowerFrame = frame
        self.packLowerFrame()