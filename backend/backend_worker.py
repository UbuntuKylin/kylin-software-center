#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
import threading
import data
import time
from ibackend import get_backend


class BackendWorker(threading.Thread):

    # def __init__(self):
    #     super(BackendWorker, self).__init__(self)

    def run(self):
        while(True):
            if(data.isWorking == False):
                data.workMutex.acquire()
                length = len(data.workPool)
                data.workMutex.release()
                if(length > 0):
                    data.workMutex.acquire()
                    itemWidget = data.workPool.pop(0)
                    data.workMutex.release()
                    print itemWidget.software.mark
                    if(itemWidget.software.mark == data.WORK_TYPE_INSTALL):
                        data.backend.install_package(itemWidget)
                    elif(itemWidget.software.mark == data.WORK_TYPE_UPDATE):
                        data.backend.update_package(itemWidget)
                    elif(itemWidget.software.mark == data.WORK_TYPE_REMOVE):
                        data.backend.remove_package(itemWidget)
                    else:
                        pass
                    itemWidget.software.mark = ''

            time.sleep(0.5)