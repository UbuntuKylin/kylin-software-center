#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'

import data
from backend.ibackend import get_backend
from backend.backend_apt import BackendApt
from backend.backend_worker import BackendWorker
from model.software import Software


class SoftwareBO:

    def get_all_software(self):
        return data.backend.get_all_packages()

    def get_software_by_name(self, softwareName):
        return data.backend.get_package_by_name(softwareName)

    def install_software(self, itemWidget):
        # software = self.get_software_by_name(softwareName.ui.name.text())
        itemWidget.software.mark = data.WORK_TYPE_INSTALL
        data.backend.add_work(itemWidget)

    def update_software(self, itemWidget):
        # software = self.get_software_by_name(softwareName)
        itemWidget.software.mark = data.WORK_TYPE_UPDATE
        data.backend.add_work(itemWidget)

    def remove_software(self, itemWidget):
        # software = self.get_software_by_name(softwareName.ui.name.text())
        itemWidget.software.mark = data.WORK_TYPE_REMOVE
        data.backend.add_work(itemWidget)

    def testinstall(self, softwareName):
        data.backend.install_package(data.backend.get_package_by_name(softwareName).package)


def main():
    w = BackendWorker()
    w.start()

    b = SoftwareBO()
    l = b.get_all_software()
    b.install_software("gedit")
    # for software in l:
    #     if(isinstance(software,Software)):
    #         print software.name
    cmd = raw_input()
    b.install_software("steam")
    # from time import time
    # start = time()
    # print("Start: " + str(start))
    # print b.get_software_by_name("gedit")
    # stop = time()
    # print("Stop: " + str(stop))
    # print(str(stop-start) + "秒")


if __name__ == '__main__':
    main()