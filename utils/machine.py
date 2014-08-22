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

import os
import platform
from models.globals import Globals


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
        uf.close()
        return rtn
    else:
        dist = platform.dist()
        distname = dist[0]
        distversion = dist[1]
        return [distname, distversion]

# uksc version
def get_uksc_version():
    return Globals.UKSC_VERSION


def main():
    print get_machine_id()
    print get_distro_info()
    print get_uksc_version()

if __name__ == '__main__':
    main()
