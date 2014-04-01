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


import aptsources.sourceslist


class SourceList:

    # get all source item in /etc/apt/sources.list
    def get_sources(self):
        slist = []
        source = aptsources.sourceslist.SourcesList()
        for one in source.list:
            if(one.disabled == False and one.type != ""):
                slist.append(one)
        return slist

    def get_sources_except_ubuntu(self):
        slist = []
        source = aptsources.sourceslist.SourcesList()
        for one in source.list:
            if(one.disabled == False and one.type != "" and one.str().find(".ubuntu.com/ubuntu") == -1):
                slist.append(one)
        return slist

    # add source into /etc/apt/sources.list
    def add_source(self, text):
        source = aptsources.sourceslist.SourcesList()
        for item in source.list:
            if(item.str().find(text) != -1):
                return

        slist = text.split()
        if(len(slist) < 3): # wrong source text
            return

        type = slist[0]
        uri = slist[1]
        dist = slist[2]
        comps = []
        for i in range(3, len(slist)):
            comps.append(slist[i])
        source.add(type, uri, dist, comps)
        source.save()

    # remove source from /etc/apt/sources.list
    def remove_source(self, text):
        source = aptsources.sourceslist.SourcesList()
        sources = source.list
        for item in sources:
            if(item.str().find(text) != -1):
                source.remove(item)
        source.save()

def main():
    sl = SourceList()
    l = sl.get_sources()
    one = l[4]
    print one.uri
    print one.invalid
    print one.disabled
    print one.type
    print one.dist
    print one.comps
    print one.comment
    print one.line
    print one.str()

if __name__ == "__main__":
    main()