#!/usr/bin/env python

from Tkinter import *

from config import globals


class upperFrame(Frame):
    """

    """
    def __init__(self, master):
        Frame.__init__(self, master, width=800)
        self.parent = master
        self.boardFrame = None
        self.running = False
        self.addWidgets()

    def addWidgets(self):
        self.displayBoard()

    def displayBoard(self):
        """
        Displays environment board
        :return:
        """
        self.boardFrame = Canvas(self, width=710, height=200)
        self.boardFrame.create_line(10, 100, 710, 100, width=2, arrow='last')
        self.boardFrame.create_line(10, 70, 10, 130, width=2)
        self.boardFrame.pack(side=LEFT, fill=Y, padx=10, pady=10)

    def resetBoard(self):
        """
        Resets environment board
        :return:
        """
        self.boardFrame.destroy()
        self.currentCoord = 10 # set time back
        self.boardFrame = Canvas(self, width=710, height=200)
        self.boardFrame.create_line(10, 100, 710, 100, width=2, arrow='last')
        self.boardFrame.create_line(10, 70, 10, 130, width=2)
        self.boardFrame.pack(side=LEFT, fill=Y, padx=10, pady=10)

    def displayRun(self):
        """
        Runs game
        :return:
        """
        if self.running:
            self.boardFrame.create_line(globals.gIteration + 11, 80, globals.gIteration + 11, 120, width=1)
            #self.boardFrame.create_line(self.currentCoord, 80, self.currentCoord, 120, width=1)