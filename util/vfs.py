#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
import os
import statvfs


def get_available_size():
    vfs=os.statvfs("/")
    available=vfs[statvfs.F_BAVAIL]*vfs[statvfs.F_BSIZE]/(1000*1000*1000)
    return str(available) + "G"
    # capacity=vfs[statvfs.F_BLOCKS]*vfs[statvfs.F_BSIZE]/(1000*1000*1000)
    # print capacity
    # used=capacity-available
    # print used