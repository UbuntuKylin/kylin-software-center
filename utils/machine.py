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


# the machine-id which from dbus calculates
def get_machine_id():
    fpath = '/var/lib/dbus/machine-id'
    if(os.path.exists(fpath) and os.path.isfile(fpath)):
        f = open(fpath, 'r')
        id = f.read()
        f.close()
        id = id.replace('\n','')
        if(id == ''):
            return 'unknown'
        else:
            return id
    else:
        return 'unknown'

# the linux distribution of this machine
def get_distro_info():
    ufpath = '/etc/ubuntukylin-release'
    if(os.path.exists(ufpath) and os.path.isfile(ufpath)):
        pass
    else:
        dist = platform.dist()
        distname = dist[0]
        return distname

def main():
    print get_machine_id()
    print get_distro_info()

if __name__ == '__main__':
    main()
