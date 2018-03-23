#!/usr/bin/env python

from Tkinter import *
from ext import globals


class timeFrame(Frame):
    def __init__(self, master, root):
        Frame.__init__(self, master, width=600, height=200)
        self.root = root # mainWindow frame
        self.parent = master
        self.timeVariableFrame = None
        self.time = IntVar()
        self.timeVariableChoice()

    def timeVariableChoice(self):
        # Variable initialization
        self.timeVariableFrame = LabelFrame(self, text="Time Variable", padx=10, pady=10)
        self.time.set(globals.gTime)

        # Widgets declaration
        labelTime = Label(self.timeVariableFrame, text="Choose type", font=("", 14))
        radioDiscrete = Radiobutton(self.timeVariableFrame, text="Discrete", variable=self.time, value=0)
        radioContinuous = Radiobutton(self.timeVariableFrame, text="Continuous", variable=self.time, value=1)

        # Widgets display
        labelTime.grid(row=0, column=0)
        radioDiscrete.grid(row=1, column=0, columnspan=2, sticky=W)
        radioContinuous.grid(row=2, column=0, columnspan=2, sticky=W)

        self.timeVariableFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)