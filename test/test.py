#!/usr/bin/python

import dbus
import gobject

from aptdaemon import client

from defer import inline_callbacks
from aptdaemon import policykit1


from PyQt4.QtCore import *
from PyQt4.QtGui import *
loop = gobject.MainLoop()

def on_finished(trans, exit):
    loop.quit()
    print exit

@inline_callbacks
def main():
    repo = ["deb", "http://packages.glatzor.de/silly-packages", "sid", ["main"],
            "Silly packages", "silly.list"]
    aptclient = client.AptClient()
    bus = dbus.SystemBus()
    name = bus.get_unique_name()
    # high level auth
    try:
        # Preauthentication
        action = policykit1.PK_ACTION_INSTALL_PURCHASED_PACKAGES
        flags = policykit1.CHECK_AUTH_ALLOW_USER_INTERACTION
        yield policykit1.check_authorization_by_name(name, action, flags=flags)
        print "111111"
        action = policykit1.PK_ACTION_INSTALL_FILE
        yield policykit1.check_authorization_by_name(name, action, flags=flags)
        print "222222"
        # Setting up transactions
        trans_add = yield aptclient.add_repository(*repo)
        trans_inst = yield aptclient.install_packages(["gimp"])
        yield trans_inst.set_allow_unauthenticated(True)
        # Check when the last transaction was done
        trans_inst.connect("finished", on_finished)
        # Chaining transactions
        yield trans_inst.run_after(trans_add)
        yield trans_add.run()
    except Exception as error:
        print error
        loop.quit()

if __name__ == "__main__":
    # main()
    # loop.run()
    # a = []
    # print a
    # del a[1231:]
    # print a
    # import aptsources.sourceslist
    # source = aptsources.sourceslist.SourcesList()
    # sources = source.list
    # for item in sources:
        # print type(item)
        # print item.str()

    import sys
    # import os
    # os.execv("/usr/bin/python", ["foo", "/home/shine/PycharmProjects/ubuntu-kylin-software-center/test/restarttext.py"])
    # la = []
    # la.append(1)
    # la.append(2)
    # la.append(5)
    # la.append(7)
    # la.append(4)
    # la.append(3)
    # sorted(la,)
    # print la

    # import time
    # print time.strftime('%Y-%m-%d',time.localtime())

    db = QFontDatabase()
    for fm in db.families():
        print fm

    # for f in fm:
    #     print f