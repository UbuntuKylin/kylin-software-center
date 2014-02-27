#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'


class AD:
    name = ''   # ad name
    type = ''   # package: pkg    websitelink: url
    pic = ''    # downloaded pic url
    urlorpkgid = '' # url or a package name

    def __init__(self, name, type, pic, urlorpkgid):
        self.name = name
        self.type = type
        self.pic = pic
        self.urlorpkgid = urlorpkgid