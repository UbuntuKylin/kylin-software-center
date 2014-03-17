#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
# Maintainer:
#     Shine Huang<shenghuang@ubuntukylin.com>

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


class History:
    hlist = ''
    hindex = ''

    ui = ''

    def __init__(self, ui):
        self.hlist = []
        self.hindex = -1
        self.ui = ui

    def history_add(self, func, parm=None):
        self.ui.btnBack.setEnabled(True)
        self.ui.btnNext.setEnabled(False)

        del self.hlist[self.hindex + 1:]
        self.hlist.append((func, parm))
        self.hindex = len(self.hlist) - 1

        if(self.hindex == 0):
            self.ui.btnBack.setEnabled(False)

    def history_back(self):
        self.ui.btnNext.setEnabled(True)

        back = self.hlist[self.hindex - 1]
        func = back[0]
        parm = back[1]
        if(parm == None):
            func(ishistory=True)
        else:
            func(parm, ishistory=True)
        self.hindex -= 1

        if(self.hindex == 0):
            self.ui.btnBack.setEnabled(False)

    def history_next(self):
        self.ui.btnBack.setEnabled(True)

        next = self.hlist[self.hindex + 1]
        func = next[0]
        parm = next[1]
        if(parm == None):
            func(ishistory=True)
        else:
            func(parm, ishistory=True)
        self.hindex += 1

        if(self.hindex == len(self.hlist) - 1):
            self.ui.btnNext.setEnabled(False)