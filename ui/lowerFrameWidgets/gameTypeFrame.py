#!/usr/bin/env python

from tkinter import *
from config import globals


class gameTypeFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=600, height=200)
        self.parent = master
        self.type = IntVar()
        self.gameTypeFrame = None
        self.gameTypeChoice()

    def gameTypeChoice(self):
        # Variable initialization
        self.gameTypeFrame = LabelFrame(self, text="Game Type", padx=10, pady=10)
        self.type.set(globals.gContinuous)

        # Widgets declaration
        radioDiscrete = Radiobutton(self.gameTypeFrame, text="Discrete", variable=self.type, value=0)
        radioContinuous = Radiobutton(self.gameTypeFrame, text="Continuous", variable=self.type, value=1, state='disabled')

        # Widgets display
        radioDiscrete.grid(row=0, column=0, columnspan=2, sticky=W)
        radioContinuous.grid(row=1, column=0, columnspan=2, sticky=W)

        self.gameTypeFrame.pack(side=LEFT, fill=BOTH, expand=1, padx=5, pady=5)