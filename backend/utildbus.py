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
import errno
import apt
import shutil
import logging
import xapian
import dbus
import dbus.service
import getpass

class UtilDbus(dbus.service.Object):

    def __init__(self, parent, bus_name,
                 object_path='/com/kylin/softwarecenter'):
        dbus.service.Object.__init__(self, bus_name, object_path)
        self.parent = parent

    def stop(self):
        """ stop the dbus controller and remove from the bus """
        self.remove_from_connection()

    @dbus.service.method('com.kylin.utiliface')
    def bring_to_front(self):
        self.parent.show_to_frontend()

    @dbus.service.method('com.kylin.utiliface', in_signature='s', out_signature='')
    def show_deb_file(self, path):
        self.parent.slot_show_deb_detail(str(path))

    @dbus.service.method('com.kylin.utiliface', in_signature='s', out_signature='')
    def show_remove_soft(self, name):
        self.parent.slot_show_remove_soft(str(name))

    @dbus.service.method('com.kylin.utiliface')
    def show_loading_div(self):
        self.parent.slot_show_loading_div()

    @dbus.service.method('com.kylin.utiliface',in_signature='s', out_signature='')
    def close_software(self,DETH):
        if DETH == "-quit":
            self.parent.slot_close()

    @dbus.service.method('com.kylin.utiliface')#//获取安全配置文件存放路径
    def GetSecurityConfigPath(self):
        dest="home"+getpass.getuser()+".config/kylin-software-center-security-config.json"


    def ReloadSecurityConfig(self):#// 重新加载安全配置（软件商店只提供接口，动态重载后续开发）
        pass
