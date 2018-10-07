#!/usr/bin/env python

from Tkinter import *

from config import globals

boardColor = ['red3', 'medium blue']

class upperFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=800)
        self.parent = master
        self.boardFrame = None
        self.startCoord = 11
        self.displayBoard()

    def displayBoard(self):
        """
        Displays environment board
        :return:
        """
        self.boardFrame = Canvas(self, width=710, height=200)
        self.boardFrame.create_line(10, 100, 710, 100, width=3, arrow='last')
        self.boardFrame.create_line(10, 50, 10, 150, width=3)
        self.boardFrame.grid(row=1, column=1)

    def resetBoard(self):
        """
        Resets environment board
        :return:
        """
        self.boardFrame.destroy()
        self.startCoord = 11 # set time back
        self.displayBoard()

    def displayRun(self):
        """
        Runs game
        :return:
        """
        self.startCoord += 1
        self.boardFrame.create_line(self.startCoord, 60 + globals.gCurrentOwner.id * 41, \
                                    self.startCoord, 99 + globals.gCurrentOwner.id * 43, \
                                    width=1, fill=boardColor[globals.gCurrentOwner.id])

        if globals.gInteractive: # add overlay
            self.boardFrame.create_line(self.startCoord, 60, self.startCoord, 142, \
                                        width=1, tags='overlay')

        if self.startCoord == 700:
            self.resetBoard()


    def showFlips(self):
        """
        Show flips on board
        :return:
        """
        self.boardFrame.delete('overlay') # destroy overlay
        self.boardFrame.itemconfig('flips', state=NORMAL) # show previous flips
        # TODO add border at each flip (detail)

    def addFlip(self, agent):
        """
        Adds flip on board
        :param agent:
        :return:
        """
        if globals.gInteractive:
            display=HIDDEN
        else:
            display=NORMAL

        self.boardFrame.create_oval(self.startCoord - 5, 35 + agent.id * (143 - 25), self.startCoord + 5, \
                                    45 + agent.id * (143 - 25), fill=boardColor[agent.id], \
                                    width=2, outline="black", tags='flips', state=display)