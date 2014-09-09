import os
import sys
import glob
from distutils.core import setup
#from DistUtilsExtra.command import build_extra
#import build_i18n_ext as build_i18n

setup(name="ubuntu-kylin-software-center",
      version="0.3.4",
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
    ('share/applications/',['ubuntu-kylin-software-center.desktop']),
    ('share/pixmaps/',['ubuntu-kylin-software-center.svg']),
    ('share/ubuntu-kylin-software-center-daemon/', glob.glob('backend/aptdaemon/dbus_service/*.py')),
    ('share/ubuntu-kylin-software-center/backend/piston/', glob.glob('backend/piston/*.py')),
    ('share/ubuntu-kylin-software-center/backend/remote/', glob.glob('backend/remote/*.py')),
    ('share/ubuntu-kylin-software-center/backend/service/', glob.glob('backend/service/*.py')),
    ('share/ubuntu-kylin-software-center/backend', glob.glob('backend/*.py')),
    ('share/ubuntu-kylin-software-center/data/ads/', glob.glob('data/ads/*.png')),
#    ('share/ubuntu-kylin-software-center/data/category/', glob.glob('data/category/*')),
    ('share/ubuntu-kylin-software-center/data/icons/', glob.glob('data/icons/*.png')),
#    ('share/ubuntu-kylin-software-center/data/screenshots/', glob.glob('data/screenshots/*')),
    ('share/ubuntu-kylin-software-center/data/tmpicons/', glob.glob('data/tmpicons/*')),
    ('share/ubuntu-kylin-software-center/data/winicons/', glob.glob('data/winicons/*')),
    ('share/ubuntu-kylin-software-center/data/', ['data/uksc.db']),
    ('share/ubuntu-kylin-software-center/data/ukscsource_db/',  glob.glob('data/ukscsource_db/*')),
    ('share/ubuntu-kylin-software-center/models/', glob.glob('models/*')),
    ('share/ubuntu-kylin-software-center/res/', glob.glob('res/*.png')),
    ('share/ubuntu-kylin-software-center/res/', glob.glob('res/*.gif')),
    ('share/ubuntu-kylin-software-center/res/loading/', glob.glob('res/loading/*')),
    ('share/ubuntu-kylin-software-center/test/', glob.glob('test/*')),
    ('share/ubuntu-kylin-software-center/ui/', glob.glob('ui/*')),
    ('share/ubuntu-kylin-software-center/utils/', glob.glob('utils/*')),
    ('share/ubuntu-kylin-software-center/',['ReadMe','ubuntu-kylin-software-center.py']),
    ('../etc/xdg/autostart/',['ubuntu-kylin-software-center-autostart.desktop']),
    ])
