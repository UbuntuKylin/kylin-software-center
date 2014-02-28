#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'

import os
import data
from threading import Thread
from multiprocessing import Process
from apt import Cache
from model.software import Software
# from PyQt4.QtCore import *

class CheckSoftwareThread(Thread):

    # sl = []
    # scmap = {}

    def __init__(self, sll, scmap):
        Thread.__init__(self)
        # import copy
        # self.sl = copy.copy(sll)
        self.sl = sll
        self.scmap = scmap

    def check_software(self):
        slist = []
        for c in os.listdir("res/category"):
            file = open(os.path.abspath("res/category/"+c), 'r')
            for line in file:
                slist.append(line[:-1])

        i = 0
        while i < len(self.sl):
            name = self.sl[i].name
            # name = "haha"
            for name_ in slist:
                if name == name_:
                    self.sl[i].category = self.scmap[name]
                    break
            else:
                self.sl.pop(i)
                i -= 1

            i += 1

        # print len(self.sl)
        data.softwareList = self.sl
        # self.emit(SIGNAL("chksoftwareover"), self.sl)

    def run(self):
        self.check_software()