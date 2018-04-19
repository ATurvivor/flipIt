#!/usr/bin/env python

from Tkinter import *

from config import globals


class timeFrame(Frame):
    def __init__(self, master, root):
        Frame.__init__(self, master, width=600, height=200)
        self.root = root # mainWindow frame
        self.parent = master
        self.timeVariableFrame = None
        self.time = IntVar()
        self.probability = StringVar() # TODO complete
        self.timeVariableChoice()

    def timeVariableChoice(self):
        # Variable initialization
        self.timeVariableFrame = LabelFrame(self, text="Time Variable", padx=10, pady=10)
        self.time.set(globals.gFiniteTime)

        # Widgets declaration
        labelTime = Label(self.timeVariableFrame, text="Choose type", font=("", 14))
        labelP = Label(self.timeVariableFrame, text="Probability : ", font=("", 12))
        radioInfinite = Radiobutton(self.timeVariableFrame, text="Infinite", variable=self.time, value=0)
        radioFinite = Radiobutton(self.timeVariableFrame, text="Finite", variable=self.time, value=1)
        entryProbability = Entry(self.timeVariableFrame, textvariable=self.probability, width=10)

        # Widgets display
        labelTime.grid(row=0, column=0)
        radioInfinite.grid(row=1, column=0, columnspan=2, sticky=W)
        radioFinite.grid(row=2, column=0, columnspan=2, sticky=W)
        labelP.grid(row=3, column=0, sticky=W)
        entryProbability.grid(row=3, column=1, columnspan=2, sticky=W)

        self.timeVariableFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)