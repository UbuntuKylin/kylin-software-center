#!/usr/bin/python
__author__ = 'Shine Huang'
import threading

print "db init..."

# used backend package manager
backend_type = 'apt'
# all software in sourcelist
softwareList = []
# counts
installedCount = -1
upgradableCount = -1
# how many softwares show in a setp
showSoftwareStep = 20
# package backend work pool
workPool = []
# True : when pool not empty, thread stop
isWorking = False

# work type enum
WORK_TYPE_INSTALL = 'i'
WORK_TYPE_UPDATE = 'u'
WORK_TYPE_REMOVE = 'r'

# work pool mutex
workMutex = threading.RLock()

# global backend & service
from backend.ibackend import get_backend
from service.software_bo import SoftwareBO
backend = get_backend()
sbo = SoftwareBO()

# task view
taskWidget = ''

testint = 0