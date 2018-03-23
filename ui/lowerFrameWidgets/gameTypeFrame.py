#!/usr/bin/env python

from Tkinter import *
from ext import globals


class gameTypeFrame(Frame):
    def __init__(self, master, root):
        Frame.__init__(self, master, width=600, height=200)
        self.root = root # mainWindow frame
        self.parent = master
        self.gameTypeFrame = None
        self.type = IntVar()
        self.probability = StringVar() # TODO complete
        self.gameTypeChoice()

    def gameTypeChoice(self):
        # Variable initialization
        self.gameTypeFrame = LabelFrame(self, text="Game Type", padx=10, pady=10)
        self.type.set(globals.gGameType)

        # Widgets declaration
        labelGame = Label(self.gameTypeFrame, text="Choose game type", font=("", 14))
        labelP = Label(self.gameTypeFrame, text="Probability : ", font=("", 12))
        radioFinite = Radiobutton(self.gameTypeFrame, text="Finite", variable=self.type, value=0)
        radioInfinite = Radiobutton(self.gameTypeFrame, text="Infinite", variable=self.type, value=1)
        entryProbability = Entry(self.gameTypeFrame, textvariable=self.probability, width=10) # entryP.focus_set(), int(entryP.get())

        # Widgets display
        labelGame.grid(row=0, column=0, columnspan=2, sticky=W)
        radioFinite.grid(row=1, column=0, columnspan=2, sticky=W)
        radioInfinite.grid(row=2, column=0, columnspan=2, sticky=W)
        labelP.grid(row=3, column=0, sticky=W)
        entryProbability.grid(row=3, column=1, columnspan=2, sticky=W)

        self.gameTypeFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)