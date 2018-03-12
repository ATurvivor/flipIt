# -*- coding: utf-8 -*-

from Tkinter import *
from ui.optionsFrame import optionsFrame

class MainWindow(Frame):
    """
    Frame containing all elements
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        #self.top_menu = TopMenu(self)
        #self.upper_frame = UpperFrame(self)
        self.top_menu = None
        self.upper_frame = None
        self.lower_frame = optionsFrame(self)
        self.pack_elements()

    def pack_upper_frame(self):
        if self.upper_frame:
            self.upper_frame.pack(side=TOP, padx=10, pady=10)

    def pack_lower_frame(self):
        if self.lower_frame:
            self.lower_frame.pack(side=BOTTOM, padx=10, pady=10)

    def pack_elements(self):
        self.pack_upper_frame()
        self.pack_lower_frame()

    def set_upper_frame(self, frame):
        """
        Change the upper_frame
        :param frame: widget that will replace the old one
        """
        if self.upper_frame:
            self.upper_frame.destroy()
        self.upper_frame = frame
        self.pack_upper_frame()

    def set_lower_frame(self, frame):
        """
        Change the lower_frame
        :param frame: widget that will replace the old one
        """
        if self.lower_frame:
            self.lower_frame.destroy_elements()
            self.lower_frame.destroy()
        self.lower_frame = frame
        self.pack_lower_frame()

    def set_mode(self, mode):
        self.upper_frame.left_frame.mode.set(mode)