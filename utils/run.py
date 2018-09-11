#!/usr/bin/python3
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
import xdg.DesktopEntry
from models.enums import Specials

import subprocess

def RemoveArgs(Execline):
    NewExecline = []
    for elem in Execline:
        elem = elem.replace("'","")
        elem = elem.replace("\"", "")
        if elem not in Specials:
            print(elem)
            NewExecline.append(elem)
    return NewExecline

# Actually execute the command

def Execute(cmd):
    if isinstance( cmd, str ) or isinstance( cmd, str):
        if (cmd.find("/home/") >= 0) or (cmd.find("su-to-root") >= 0) or (cmd.find("\"") >= 0):
            print("running manually...")
            try:
                os.system(cmd + " &")
                return True
            except Exception as detail:
                print(detail)
                return False
    cmd = cmd.split()
    cmd = RemoveArgs(cmd)

    try:
        string = ' '.join(cmd)
        string = string + " &"
        #subprocess.Popen( cmd ) // use os.system instead of popen so children don't end up in zombie waiting for us to wait() for them
        os.system(string)
        return True
    except Exception as detail:
        print(detail)
        return False


def get_run_command(pkgname):
    # 对一些特殊软件单独处理
    if pkgname == 'wps-office':
        pkgname = 'wps-office-wps'
    elif pkgname == 'uget':
        pkgname = 'uget-gtk'
    elif pkgname == 'eclipse-platform':
        pkgname = 'eclipse'
    elif pkgname == 'software-center':
        pkgname = 'ubuntu-software-center'
    elif pkgname == "sogoupinyin":
        pkgname = "fcitx-ui-sogou-qimpanel"
    elif pkgname == "mathwar":
        pkgname = "MathWar"
    elif pkgname == "gnome-disk-utility":
        pkgname = "gnome-disks"
    elif pkgname == "kino":
        pkgname = "Kino"
    elif pkgname == "monajat-applet":
        pkgname = "monajat"
    elif pkgname == "system-config-printer-applet":
        pkgname = "system-config-printer"
    elif pkgname == "xterm":
        pkgname = "debian-uxterm"
    elif pkgname == "virtualbox-qt":
        pkgname = "virtualbox"
    elif pkgname == "lovewallpaper":
        pkgname = "love-wallpaper"
    elif pkgname == "steam-launcher":
        pkgname = "steam"
    elif pkgname == "obs-studio":
        pkgname = "obs"
    elif pkgname == "google-chrome-stable":
        pkgname = "google-chrome"
#crossover:i386
    elif pkgname == "crossover:i386":
        pkgname = "/opt/cxoffice/bin/crossover"

    # fd = os.popen('find /usr/share/applications/ -name "%s.desktop" | xargs grep "Exec"' %pkgname)
    # exc = fd.read()
    # fd.close()
    fullcmd = ""
    desktopfile = "/usr/share/applications/" + pkgname + ".desktop"
    if not os.path.exists(desktopfile):
        if pkgname == "gnome-screenshot":
            pkgname = "org.gnome.Screenshot"
        if pkgname == "gnome-mines":
            pkgname = "gnomine"
        desktopfile = "/usr/share/applications/" + pkgname + ".desktop"
    if os.path.exists(desktopfile):
        DeskTopEntry = xdg.DesktopEntry.DesktopEntry(desktopfile)
        fullcmd = DeskTopEntry.getExec()

    # command = ['']
    # # 截取运行指令部分
    # if exc:
    #     command = re.findall('Exec=(.*)',exc)
    # print command,"000000000000000000000"
    # # 有些软件Exec后面会有%U %f等，进行过滤
    # if re.findall(' ',command[0]):
    #     command = re.findaqll('(.*) ',command[0])
    #     print command,"111111111111111111111111"
    # #split the command to prevent the error: "OSError: [Errno 2] 没有那个文件或目录"
    # fullcmd = command[0]
    # print fullcmd,"2222222222222222222"
    # if fullcmd:
    #     fullcmd = command[0].split()
    return fullcmd

def run_app(pkgname):
    cmd = get_run_command(pkgname)
    if cmd != "":
        print(("\n#####run_app:",cmd))
        Execute(cmd)
    # #p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    # os.system(cmd[0] + "&")#fixed bug 1402953

def run_appa():
    p = subprocess.Popen(["eog", "/home/shine/Downloads/009-01.png"], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)


def judge_app_run_or_not(pkgname):
    result = 0
    cmd = get_run_command(pkgname)
    if cmd[0] is not None:
        cmd = 'pgrep -f ' + cmd[0] + ' | wc -l'
        ps = os.popen(cmd)
        result = int(ps.read().replace('/n', ''))
        ps.close()
    return result

def main():
    run_appa()

if __name__ == '__main__':
    main()
