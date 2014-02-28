#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Shine Huang'
import data


class Software:
    # easy reading name in our control
    popularName = ''

    category = ''
    id_ = ''
    icon = ''
    avgGrade = ''
    downloadTimes = ''

    package = ''
    itemWidget = ''

    mark = ''

    @property
    def name(self):
        if(data.backend_type == 'apt'):
            return self.package.name
        if(data.backend_type == 'packagekit'):
            return self.package.XXXX

    @property
    def description(self):
        if(data.backend_type == 'apt'):
            return self.package.candidate.description
        if(data.backend_type == 'packagekit'):
            return self.package.XXXX

    @property
    def summary(self):
        if(data.backend_type == 'apt'):
            return self.package.candidate.summary
        if(data.backend_type == 'packagekit'):
            return self.package.XXXX

    @property
    def packageSize(self):
        if(data.backend_type == 'apt'):
            return self.package.candidate.size
        if(data.backend_type == 'packagekit'):
            return self.package.XXXX

    @property
    def is_installed(self):
        if(data.backend_type == 'apt'):
            return self.package.is_installed
        if(data.backend_type == 'packagekit'):
            return self.package.XXXX

    @property
    def is_upgradable(self):
        if(data.backend_type == 'apt'):
            return self.package.is_upgradable
        if(data.backend_type == 'packagekit'):
            return self.package.XXXX

    @property
    def installed_size(self):
        if(data.backend_type == 'apt'):
            return self.package.candidate.installed_size
        if(data.backend_type == 'packagekit'):
            return self.package.XXXX

    @property
    def candidate_version(self):
        if(data.backend_type == 'apt'):
            return self.package.candidate.version
        if(data.backend_type == 'packagekit'):
            return self.package.XXXX

    @property
    def installed_version(self):
        if(data.backend_type == 'apt'):
            if(self.package.installed != None):
                return self.package.installed.version
            else:
                return ""
        if(data.backend_type == 'packagekit'):
            return self.package.XXXX