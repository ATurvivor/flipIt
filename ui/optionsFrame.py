# -*- coding: utf-8 -*-

from Tkinter import *

class optionsFrame(Frame):
    """

    """
    def __init__(self, master):
        Frame.__init__(self, master, width=500, height=200)
        self.parent = master
        self.strategyP1 = IntVar()
        self.strategyP2 = IntVar()
        self.strategyChoiceFrame = None
        self.gameTypeFrame = None
        self.addWidgets()

    def addWidgets(self):
        self.strategyChoice()
        #self.gameType()

    def strategyChoice(self):
        # Variable initialization
        self.strategyChoiceFrame = LabelFrame(self, text="Agents")
        self.strategyP1.set(0)
        self.strategyP2.set(0)

        # Widgets declaration
        labelStrategy = Label(self.strategyChoiceFrame, text="Choose strategies:", font=("", 14))
        labelS1 = Label(self.strategyChoiceFrame, text="Player 1", font=("", 12))
        labelS2 = Label(self.strategyChoiceFrame, text="Player 2", font=("", 12))

        radioRandom1 = Radiobutton(self.strategyChoiceFrame, text="Random", variable=self.strategyP1, value=0)
        radioAdaptive1 = Radiobutton(self.strategyChoiceFrame, text="Adaptive", variable=self.strategyP1, value=1)

        radioRandom2 = Radiobutton(self.strategyChoiceFrame, text="Random", variable=self.strategyP2, value=0)
        radioAdaptive2 = Radiobutton(self.strategyChoiceFrame, text="Adaptive", variable=self.strategyP2, value=1)

        # Widgets display
        labelStrategy.grid(row=0, column=0, columnspan=4)
        labelS1.grid(row=1, column=0)
        labelS2.grid(row=1, column=2)
        radioRandom1.grid(row=2, column=0, columnspan=2, sticky=W)
        radioAdaptive1.grid(row=3, column=0, columnspan=2, sticky=W)
        radioRandom2.grid(row=2, column=2, columnspan=2, sticky=W)
        radioAdaptive2.grid(row=3, column=2, columnspan=2, sticky=W)

        self.strategyChoiceFrame.pack(side=LEFT,fill=Y, padx=10, pady=10)