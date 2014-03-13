import os
import sys
import glob
from distutils.core import setup
#from DistUtilsExtra.command import build_extra
#import build_i18n_ext as build_i18n

setup(name="ubuntu-kylin-software-center",
      version="0.2.2",
      author="Ubuntu Kylin Team",
      author_email="ubuntukylin-members@list.launchpad.net",
      url="https://launchpad.net/ubuntu-kylin-software-center",
      license="GNU General Public License (GPL)",
      data_files=[
    ('bin/', ['ubuntu-kylin-software-center']),
    ('../etc/dbus-1/system.d/', ['backend/aptdaemon/conf/com.ubuntukylin.softwarecenter.conf']),
    ('share/dbus-1/system-services/', ['backend/aptdaemon/conf/com.ubuntukylin.softwarecenter.service']),
    ('share/polkit-1/actions/', ['backend/aptdaemon/conf/com.ubuntukylin.softwarecenter.policy']),
#    ('lib/python2.7/dist-packages/ubuntu-kylin-software-center-daemon/', ['backend/aptdaemon/dbus_service/start_systemdbus.py']),
    ('share/applications/',['ubuntu-kylin-software-center.desktop'])
    ('share/pixmaps/',['ubuntu-kylin-software-center.svg'])
    ('share/ubuntu-kylin-software-center-daemon/', glob.glob('backend/aptdaemon/dbus_service/*.py')),
    ('../opt/ubuntu-kylin-software-center/backend/piston/', glob.glob('backend/piston/*.py')),
    ('../opt/ubuntu-kylin-software-center/backend', glob.glob('backend/*.py')),
    ('../opt/ubuntu-kylin-software-center/data/ads/', glob.glob('data/ads/*.png')),
    ('../opt/ubuntu-kylin-software-center/data/category/', glob.glob('data/category/*')),
    ('../opt/ubuntu-kylin-software-center/data/icons/', glob.glob('data/icons/*.png')),
    ('../opt/ubuntu-kylin-software-center/data/screenshots/', glob.glob('data/screenshots/*')),
    ('../opt/ubuntu-kylin-software-center/data/tmpicons/', glob.glob('data/tmpicons/*')),
    ('../opt/ubuntu-kylin-software-center/data/', ['data/__init__.py','data/search.py']),
    ('../opt/ubuntu-kylin-software-center/models/', glob.glob('models/*')),
    ('../opt/ubuntu-kylin-software-center/res/', glob.glob('res/*')),
    ('../opt/ubuntu-kylin-software-center/test/', glob.glob('test/*')),
    ('../opt/ubuntu-kylin-software-center/ui/', glob.glob('ui/*')),
    ('../opt/ubuntu-kylin-software-center/utils/', glob.glob('utils/*')),
    ('../opt/ubuntu-kylin-software-center/',['ReadMe','softwarecenter.py']),
    ])
