#!/usr/bin/env python

from Tkinter import *

from config import globals

boardColor = ['red3', 'medium blue']

class upperFrame(Frame):
    """

    """
    def __init__(self, master):
        Frame.__init__(self, master, width=800)
        self.parent = master
        self.boardFrame = None
        self.it=0
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
        self.currentCoord = 10 # set time back
        self.displayBoard()

    def displayRun(self):
        """
        Runs game
        :return:
        """
        self.boardFrame.create_line(globals.gIteration + 11, 60 + globals.gCurrentOwner.id * 41,\
                                    globals.gIteration + 11, 99 + globals.gCurrentOwner.id * 43,\
                                    width=1, fill=boardColor[globals.gCurrentOwner.id])

        if globals.gInteractive: # add overlay
            self.boardFrame.create_line(globals.gIteration + 11, 60, globals.gIteration + 11, 142,\
                                        width=1, tags='line{}'.format(self.it))

    def showFlips(self):
        """
        Show flips on board
        :return:
        """
        self.boardFrame.delete('line{}'.format(self.it))

        self.addFlip(self.parent.agents[0])
        self.boardFrame.itemconfig('flips', state=NORMAL)
        self.it += 1

        # TODO add border at each flip

    def addFlip(self, agent):
        """
        Adds flip on board
        :param agent:
        :return:
        """
        if globals.gInteractive: display=HIDDEN
        else: display=NORMAL

        self.boardFrame.create_oval(globals.gIteration + 11 - 5, 35 + agent.id * (143 - 25), globals.gIteration + 11 + 5,\
                                    45 + agent.id * (143 - 25), fill=boardColor[agent.id],\
                                    width=2, outline="black", tags='flips', state=display)