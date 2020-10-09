#!/usr/bin/python3
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

import os
import platform
import locale
from models.globals import Globals
import linecache


# new version no longer send dbus id
def get_machine_id():
    # fpath = '/var/lib/dbus/machine-id'
    # if(os.path.exists(fpath) and os.path.isfile(fpath)):
    #     f = open(fpath, 'r')
    #     id = f.read()
    #     f.close()
    #     id = id.replace('\n','')
    #     if(id == ''):
    #         return 'unknown'
    #     else:
    #         return id
    # else:
    #     return 'unknown'

    return 'empty'

# the linux distribution of this machine
def get_distro_info():
    ufpath = '/etc/ubuntukylin-release'
    if(os.path.exists(ufpath) and os.path.isfile(ufpath)):
        uf = open(ufpath)
        lines = uf.readlines()
        rtn = []
        for line in lines:
            kv = line.split('=')
            if (kv[0] == 'DISTRIB_ID'):
                v = kv[1]
                rtn.append(v[:-1])
            if (kv[0] == 'DISTRIB_RELEASE'):
                v = kv[1]
                rtn.append(v[:-1])
            if (kv[0] == 'DISTRIB_CODENAME'):
                v = kv[1]
                rtn.append(v[:-1])
        uf.close()
        return rtn
    else:
        dist = get_system_name_vision()
        distname = dist[0]
        distversion = dist[1]
        distroseries = dist[2]
        return [distname, distversion, distroseries]

def get_system_name_vision():
    file_path = "/etc/os-release"
    line_number = 3
    dist = linecache.getline(file_path, line_number).strip()
    dest = []
    dest.append(dist[3:])
    file = open("/etc/os-release", "r")
    for line in file:
        if "VERSION_ID=" in line:
            str1 = line[12:].strip()
            dest.append(str1.strip('"'))
        if "UBUNTU_CODENAME" in line:
            dest.append(line[16:].strip())
    return dest

# uksc version
def get_uksc_version():
    return Globals.UKSC_VERSION

# get this os language
def get_language():
    return locale.getdefaultlocale()[0]


def main():
    if (Globals.DEBUG_SWITCH):
        print(get_machine_id())
        print(get_distro_info())
        print(get_uksc_version())
        print(get_language())

if __name__ == '__main__':
    main()
