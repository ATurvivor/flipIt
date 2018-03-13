# -*- coding: utf-8 -*-

from Tkinter import *

class upperFrame(Frame):
    """

    """
    def __init__(self, master):
        Frame.__init__(self, master, width=600)
        self.parent = master
        self.timeFrame = None
        self.addWidgets()

    def addWidgets(self):
        self.displayFlips()

    def displayFlips(self):
        # add board with colors
        self.timeFrame = Canvas(self, width=510, height=200)
        self.timeFrame.create_line(10, 100, 510, 100, width=2, arrow='last')
        self.timeFrame.create_line(10, 70, 10, 130, width=2)
        self.timeFrame.pack(side=LEFT, fill=Y, padx=10, pady=10)