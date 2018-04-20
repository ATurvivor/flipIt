#!/usr/bin/env python

from Tkinter import *

from config import globals

boardColor = ['red3', 'midnight blue']

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
        self.boardFrame.create_line(globals.gIteration + 11, 60, globals.gIteration + 11, 142,\
                                    width=1, tags='line{}'.format(self.it))
        #self.boardFrame.create_oval(globals.gIteration-5, 50 + globals.gCurrentOwner.id * 152, globals.gIteration + 5,\
                                    #60 + globals.gCurrentOwner.id * 152, fill=boardColor[globals.gCurrentOwner.id],\
                                    #width=2, outline="black", tags='flips')

    def show(self):
        self.boardFrame.delete('line{}'.format(self.it))
        self.boardFrame.create_oval(globals.gIteration + 11 - 5, 35, globals.gIteration + 11 + 5,\
                                    45, fill=boardColor[0],\
                                    width=2, outline="black", tags='flips')

        # TODO add border at each flip

        self.boardFrame.itemconfig('flips', state=NORMAL)
        self.it += 1