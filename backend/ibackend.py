#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
import data
from backend_apt import BackendApt


def get_backend():
    if (data.backend_type == 'apt'):
        return BackendApt()
    if (data.backend_type == 'packagekit'):
        #self.backend = BackendPackagekit()
        return None