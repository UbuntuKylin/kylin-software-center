#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Wen Bo<wenbo@ubuntukylin.com>
#     Shine Huang<shenghuang@ubuntukylin.com>
# Maintainer:
#     Wen Bo<wenbo@ubuntukylin.com>
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


import os
import re
import subprocess

def get_run_command(pkgname):
    fd = os.popen('find /usr/share/applications/ -name "%s.desktop" | xargs grep "Exec"' %pkgname)
    exc = fd.read()
    fd.close()
    #print exc
    # 截取运行指令部分
    if exc:
        command = re.findall('Exec=(.*)',exc)
    # 有些软件Exec后面会有%U %f等，进行过滤
    if re.findall(' ',command[0]):
        command = re.findall('(.*) ',command[0])
    #print command[0]
    return command[0]

def run_app(pkgname):
    cmd = get_run_command(pkgname)
    p = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)