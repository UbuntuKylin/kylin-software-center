 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
from setuptools import setup, Command
import DistUtilsExtra.command.build_extra
import DistUtilsExtra.command.build_i18n
import DistUtilsExtra.command.clean_i18n
from subprocess import call
#from DistUtilsExtra.command import build_extra
#import build_i18n_ext as build_i18n


PO_DIR = 'po'


class CleanCommand(DistUtilsExtra.command.clean_i18n.clean_i18n):
    user_options = [('all', None, '(Compatibility with original clean command)')]

    def initialize_options(self):
        self.all = False
        super().initialize_options()


for po in glob.glob(os.path.join(PO_DIR, '*.po')):
    lang = os.path.basename(po[:-3])
    mo = os.path.join(PO_DIR, 'ubuntu-kylin-software-center.mo')
    target_dir = os.path.dirname(mo)
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    try:
        return_code = call(['msgfmt', '-o', mo, po])
    except OSError:
        raise Warning('Translation not available, please install gettext')
        break
    if return_code:
        raise Warning('Error when building locales')
cmdclass ={
            "build" : DistUtilsExtra.command.build_extra.build_extra,
            "build_i18n" :  DistUtilsExtra.command.build_i18n.build_i18n,
            "clean": CleanCommand,
}


data_files=[
    ('bin/', ['ubuntu-kylin-software-center']),
    ('../etc/dbus-1/system.d/', ['backend/aptdaemon/conf/com.ubuntukylin.softwarecenter.conf']),
    ('share/dbus-1/system-services/', ['backend/aptdaemon/conf/com.ubuntukylin.softwarecenter.service']),
    ('share/polkit-1/actions/', ['backend/aptdaemon/conf/com.ubuntukylin.softwarecenter.policy']),
#    ('lib/python3/dist-packages/ubuntu-kylin-software-center-daemon/', glob.glob('backend/aptdaemon/dbus_service')),
    ('share/applications/',['ubuntu-kylin-software-center.desktop']),
    ('share/pixmaps/',['ubuntu-kylin-software-center.svg']),
#    ('share/ubuntu-kylin-software-center-daemon/', glob.glob('backend/aptdaemon/dbus_service/*.py')),
    ('share/ubuntu-kylin-software-center/backend/piston/', glob.glob('backend/piston/*.py')),
    ('share/ubuntu-kylin-software-center/backend/remote/', glob.glob('backend/remote/*.py')),
    ('share/ubuntu-kylin-software-center/backend/service/', glob.glob('backend/service/*.py')),
    ('share/ubuntu-kylin-software-center/backend/service/', glob.glob('backend/service/*.txt')),
    ('share/ubuntu-kylin-software-center/backend/login_impl/', glob.glob('backend/login_impl/*.py')),
    ('share/ubuntu-kylin-software-center/backend', glob.glob('backend/*.py')),
    ('share/ubuntu-kylin-software-center/data/ads/', glob.glob('data/ads/*.png')),
#    ('share/ubuntu-kylin-software-center/data/category/', glob.glob('data/category/*')),
    ('share/ubuntu-kylin-software-center/data/icons/', glob.glob('data/icons/*.png')),
#    ('share/ubuntu-kylin-software-center/data/screenshots/', glob.glob('data/screenshots/*')),
    ('share/ubuntu-kylin-software-center/data/tmpicons/', glob.glob('data/tmpicons/*')),
    ('share/ubuntu-kylin-software-center/data/winicons/', glob.glob('data/winicons/*')),
    ('share/ubuntu-kylin-software-center/data/screenshots/', glob.glob('data/screenshots/*')),
    ('share/ubuntu-kylin-software-center/data/', ['data/uksc.db']),
    ('share/ubuntu-kylin-software-center/data/xapiandb/',  glob.glob('data/xapiandb/*')),
    ('share/ubuntu-kylin-software-center/models/', glob.glob('models/*')),
    ('share/ubuntu-kylin-software-center/res/', glob.glob('res/*.png')),
    ('share/ubuntu-kylin-software-center/res/', glob.glob('res/*.gif')),
    ('share/ubuntu-kylin-software-center/res/loading/', glob.glob('res/loading/*')),
    ('share/ubuntu-kylin-software-center/test/', glob.glob('test/*')),
    ('share/ubuntu-kylin-software-center/ui/', glob.glob('ui/*')),
    ('share/ubuntu-kylin-software-center/utils/', glob.glob('utils/*')),
    ('share/ubuntu-kylin-software-center/po/', glob.glob('po/*')),
    ('share/ubuntu-kylin-software-center/kydroid/', glob.glob('kydroid/*')),
    ('share/ubuntu-kylin-software-center/',['ubuntu-kylin-software-center.py']),
    # ('../etc/xdg/autostart/',['ubuntu-kylin-software-center-autostart.desktop']),
    ]

def find_mo_files():
    data_files = []
    for mo in glob.glob(os.path.join(PO_DIR, '*', 'ubuntu-kylin-software-center.mo')):
        lang = os.path.basename(os.path.dirname(mo))
        dest = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
        data_files.append((dest, [mo]))
    return data_files

data_files.extend(find_mo_files())



setup(name="ubuntu-kylin-software-center",
    version="1.3.10",
    author="Ubuntu Kylin Team",
    author_email="ubuntukylin-members@list.launchpad.net",
    url="https://launchpad.net/ubuntu-kylin-software-center",
    license="GNU General Public License (GPL)",
    packages = [ 'ubuntu_kylin_software_center_daemon',],
    package_dir = {
        '': '.',
    },
    install_requires = [ 'setuptools', ],
    cmdclass = cmdclass,
    data_files=data_files,
)

