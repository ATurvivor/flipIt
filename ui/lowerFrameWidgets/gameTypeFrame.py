#!/usr/bin/env python

from Tkinter import *

from config import globals


class gameTypeFrame(Frame):
    def __init__(self, master, root):
        Frame.__init__(self, master, width=600, height=200)
        self.root = root # mainWindow frame
        self.parent = master
        self.gameTypeFrame = None
        self.type = IntVar()
        self.gameTypeChoice()

    def gameTypeChoice(self):
        # Variable initialization
        self.gameTypeFrame = LabelFrame(self, text="Game Type", padx=10, pady=10)
        self.type.set(globals.gGameType)

        # Widgets declaration
        labelGame = Label(self.gameTypeFrame, text="Choose game type", font=("", 14))
        radioContinuous = Radiobutton(self.gameTypeFrame, text="Continuous", variable=self.type, value=0)
        radioDiscrete = Radiobutton(self.gameTypeFrame, text="Discrete", variable=self.type, value=1)

        # Widgets display
        labelGame.grid(row=0, column=0, columnspan=2, sticky=W)
        radioContinuous.grid(row=1, column=0, columnspan=2, sticky=W)
        radioDiscrete.grid(row=2, column=0, columnspan=2, sticky=W)

        self.gameTypeFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)