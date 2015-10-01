#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-09-28 21:32:31
# @Last Modified 2015-09-30 Jeremiah@JLMarks.org
# @Last Modified time: 2015-09-30 18:51:23
import csv
from Tkinter import *


class CSVToolbox:
    """This class will provide file interactions AND a gui.
    """
    def __init__(self, parent):
        #------ constants for controlling layout of buttons ------
        button_width = 6
        button_padx = "2m"
        button_pady = "1m"
        buttons_frame_padx =  "3m"
        buttons_frame_pady =  "2m"
        buttons_frame_ipadx = "3m"
        buttons_frame_ipady = "1m"
        # -------------- end constants ----------------
        self.filename = StringVar()
        self.filename.set(NONE)

        self.myParent = parent
        self.myParent.geometry("640x400")


        self.myContainer1 = Frame(parent) ###
        self.myContainer1.pack(expand=YES, fill=BOTH)
