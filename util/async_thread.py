#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'

import os
import data
from threading import Thread
from multiprocessing import Process


class AsyncThread(Thread):
    # work function
    workFunc = ''
    args = ''

    def __init__(self, func, *args):
        Thread.__init__(self)
        self.workFunc = func
        self.args = args

    def run(self):
        if(len(self.args) == 0):
            self.workFunc()
        elif(len(self.args) == 1):
            self.workFunc(self.args[0])
        elif(len(self.args) == 2):
            self.workFunc(self.args[0], self.args[1])