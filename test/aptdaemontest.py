#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'

import apt_pkg
import dbus
import logging
import os
import re
import traceback
from subprocess import (
    Popen,
    PIPE,
)
from aptdaemon import client
from aptdaemon.client import *
from aptdaemon import enums
from aptdaemon import errors
from aptsources.sourceslist import SourceEntry
from aptdaemon import policykit1


class AptDaemonTest:

    def __init__(self):
        bus = dbus.SystemBus()
        self.aptd_client = client.AptClient(bus=bus)
        # self.aptd_client = client.AptClient()
        transaction = self.aptd_client.update_cache()
        self.aptd_client.install_packages(["alltray"])
        if(isinstance(transaction, AptTransaction)):
            transaction.set_locale("zh_CN")
            transaction.connect("finished", self.on_transaction_finished)
            transaction.run()

    def on_transaction_finished(self):
        print "aa"

    def testinstall(self):
        self.aptd_client.install_packages(["alltray"])

def main():
    aptd = AptDaemonTest()
    # aptd.testinstall()

if __name__ == '__main__':
    main()