#!/usr/bin/python
# -*- coding: utf-8 -*-
from service.software_bo import main

__author__ = 'Shine Huang'
import threading
import time
import data
mutex = threading.RLock()
class Worker(threading.Thread):

    def run(self):
        for i in range(3):
            mutex.acquire()
            data.testint += 1
            print self.getName(), "++++ task", data.testint
            time.sleep(1)
            mutex.release()

class Worker_(threading.Thread):
    def run(self):
        mutex.acquire()
        for i in range(3):
            data.testint -= 1
            print self.getName(), "---- task", data.testint
        mutex.release()


def main():
    Worker().start()
    Worker_().start()

if __name__ == '__main__':
    main()