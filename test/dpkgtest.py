__author__ = 'shine'

# from debian.debfile import *
from apt.debfile import DebPackage
# pkg = DebPackage("/home/shine/abe_1.1+dfsg-1_amd64.deb")
pkg = DebPackage("/home/shine/abe-data_1.1+dfsg-1_all.deb")
# print pkg.check()
print pkg.pkgname
print pkg._sections["Description"]
print pkg._sections["Version"]
print pkg._sections["Installed-Size"]
# print pkg.missing_deps
# pkg.install()
# print pkg.filelist