#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     maclin <majun@ubuntukylin.com>
# Maintainer:
#     maclin <majun@ubuntukylin.com>

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

import sqlite3


DB_PATH = "cat_app.db"

CREATE_CATEGORY = "create table category (id integer autoincrement   \
        primary key,name varchar(32) UNIQUE,display_name varchar(32) )"
INSERT_CATEGORY = "insert into category values(%s, %s, 'name1')")


class Database:

    def __init__(self):
        self.connect = sqlite3.connect(DB_PATH)
        self.cursor = self.connect.cursor()

    def create_category_db(self):
        self.cursor.execute()





