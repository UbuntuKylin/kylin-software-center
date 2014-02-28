#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'

import os
import data
from multiprocessing import Process, Queue


class AsyncProcess(Process):
    # work function
    workFunc = ''
    q = ''

    def __init__(self, func):
        Process.__init__(self)
        self.workFunc = func
        self.q = Queue()

    def run(self):
        self.workFunc(self.q.get())