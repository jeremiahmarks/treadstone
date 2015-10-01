#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-09-28 21:32:12
# @Last Modified 2015-09-30 Jeremiah@JLMarks.org
# @Last Modified time: 2015-09-30 18:42:22

import os
import csv

class csvworker:
    """This is the actual effector of work on the files.
    """
    def __init__(self, pathtocsv):
        self.filepath = pathtocsv

