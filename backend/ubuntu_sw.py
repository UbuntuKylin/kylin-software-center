# Copyright (C) 2009 Canonical
#
# Authors:
#  Michael Vogt
#  maclin <majun@ubuntukylin.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

# These defines of variables and classes are imported from ubuntu software center

from gettext import gettext as _
import os
import errno
import apt
import shutil
import logging
import xapian


LOG = logging.getLogger("uksc")

# reviews
 #REVIEWS_SERVER = (os.environ.get("SOFTWARE_CENTER_REVIEWS_HOST") or
#     "http://reviews.ubuntu.com/reviews/api/1.0")
 #REVIEWS_URL = (REVIEWS_SERVER + "/reviews/filter/%(language)s/%(origin)s/"
 #    "%(distroseries)s/%(version)s/%(pkgname)s%(appname)s/")

REVIEWS_SERVER = ("http://reviews.ubuntu.com/reviews/api/1.0")
REVIEWS_URL = (REVIEWS_SERVER + "%(distroseries)s/%(version)s/%(pkgname)s%(appname)s/")


#define the const screenshot_JSON_URL, copy from Ubuntu.py of ubuntu-sw
SCREENSHOT_JSON_URL = "http://screenshots.ubuntu.com/json/package/%s"

# screenshot handling
SCREENSHOT_THUMB_URL = ("http://screenshots.ubuntu.com/"
    "thumbnail-with-version/%(pkgname)s/%(version)s")
SCREENSHOT_LARGE_URL = ("http://screenshots.ubuntu.com/"
    "screenshot-with-version/%(pkgname)s/%(version)s")


# system pathes
APP_INSTALL_PATH = "/usr/share/app-install"
APP_INSTALL_DESKTOP_PATH = APP_INSTALL_PATH + "/desktop/"



#=============================================================================begin
#Added from softwarecenter.enums
# sorting
class SortMethods:
    (UNSORTED,
     BY_ALPHABET,
     BY_SEARCH_RANKING,
     BY_CATALOGED_TIME,
     BY_TOP_RATED,
    ) = range(5)


class ReviewSortMethods:
    REVIEW_SORT_METHODS = ['helpful', 'newest']
    REVIEW_SORT_LIST_ENTRIES = [_('Most helpful first'), _('Newest first')]
#=============================================================================end

#=============================================================================begin
#Added from softwarecenter.backend.reviews.__init__
#Modified:
#   replace app with pkgname
#   remove classmethod from_json
class Review(object):
    """A individual review object """
    def __init__(self, pkgname):
        # a softwarecenter.db.database.Application object
#        self.app = app
#        self.app_name = app.appname
        self.package_name = pkgname
        # the review items that the object fills in
        self.id = None
        self.language = None
        self.summary = ""
        self.review_text = ""
        self.package_version = None
        self.date_created = None
        self.rating = None
        self.reviewer_username = None
        self.reviewer_displayname = None
        self.version = ""
        self.usefulness_total = 0
        self.usefulness_favorable = 0
        # this will be set if tryint to submit usefulness for this review
        # failed
        self.usefulness_submit_error = False
        self.delete_error = False
        self.modify_error = False

    def __repr__(self):
        return "[Review id=%s review_text='%s' reviewer_username='%s']" % (
            self.id, self.review_text, self.reviewer_username)


    @classmethod
    def from_piston_mini_client(cls, other):
        """ converts the rnrclieent reviews we get into
            "our" Review object (we need this as we have more
            attributes then the rnrclient review object)
        """
        pkgname = other.package_name
        review = cls(pkgname)
        for (attr, value) in other.__dict__.items():
            if not attr.startswith("_"):
                setattr(review, attr, value)
        return review

#=============================================================================end

# values used in the database
class XapianValues:
    APPNAME = 170
    PKGNAME = 171
    ICON = 172
    GETTEXT_DOMAIN = 173
    ARCHIVE_SECTION = 174
    ARCHIVE_ARCH = 175
    POPCON = 176
    SUMMARY = 177
    ARCHIVE_CHANNEL = 178
    DESKTOP_FILE = 179
    PRICE = 180
    ARCHIVE_PPA = 181
    ARCHIVE_DEB_LINE = 182
    ARCHIVE_SIGNING_KEY_ID = 183
    PURCHASED_DATE = 184
    SCREENSHOT_URLS = 185             # multiple urls, comma seperated
    ICON_NEEDS_DOWNLOAD = 186         # no longer used
    THUMBNAIL_URL = 187               # no longer used
    SC_DESCRIPTION = 188
    APPNAME_UNTRANSLATED = 189
    ICON_URL = 190
    CATEGORIES = 191
    LICENSE_KEY = 192
    LICENSE_KEY_PATH = 193           # no longer used
    LICENSE = 194
    VIDEO_URL = 195
    DATE_PUBLISHED = 196
    SUPPORT_SITE_URL = 197
    VERSION_INFO = 198
    SC_SUPPORTED_DISTROS = 199


def safe_makedirs(dir_path):
    """ This function can be used in place of a straight os.makedirs to
        handle the possibility of a race condition when more than one
        process may potentially be creating the same directory, it will
        not fail if two processes try to create the same dir at the same
        time
    """
    # avoid throwing an OSError, see for example LP: #743003
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                # it seems that another process has already created this
                # directory in the meantime, that's ok
                pass
            else:
                # the error is due to something else, so we want to raise it
                raise

"""

def rebuild_database(pathname, debian_sources=True, appstream_sources=False):
    #cache = get_pkg_info()
    #cache.open()
    cache = apt.Cache()
    cache.open()
    old_path = pathname + "_old"
    rebuild_path = pathname + "_rb"

    if not os.path.exists(rebuild_path):
        try:
            os.makedirs(rebuild_path)
        except:
            LOG.warn("Problem creating rebuild path '%s'." % rebuild_path)
            LOG.warn("Please check you have the relevant permissions.")
            return False

    # check permission
    if not os.access(pathname, os.W_OK):
        LOG.warn("Cannot write to '%s'." % pathname)
        LOG.warn("Please check you have the relevant permissions.")
        return False

    #check if old unrequired version of db still exists on filesystem
    if os.path.exists(old_path):
        LOG.warn("Existing xapian old db was not previously cleaned: '%s'." %
            old_path)
        if os.access(old_path, os.W_OK):
            #remove old unrequired db before beginning
            shutil.rmtree(old_path)
        else:
            LOG.warn("Cannot write to '%s'." % old_path)
            LOG.warn("Please check you have the relevant permissions.")
            return False

    # write it
    db = xapian.WritableDatabase(rebuild_path, xapian.DB_CREATE_OR_OVERWRITE)

    if debian_sources:
        update(db, cache)
    if appstream_sources:
        if os.path.exists('./data/app-stream/appdata.xml'):
            update_from_appstream_xml(db, cache,
                './data/app-stream/appdata.xml')
        else:
            update_from_appstream_xml(db, cache)

    # write the database version into the filep
    db.set_metadata("db-schema-version", DB_SCHEMA_VERSION)
    # update the mo file stamp for the langpack checks
    mofile = gettext.find("app-install-data")
    if mofile:
        mo_time = os.path.getctime(mofile)
        db.set_metadata("app-install-mo-time", str(mo_time))
    db.flush()

    # use shutil.move() instead of os.rename() as this will automatically
    # figure out if it can use os.rename or needs to do the move "manually"
    try:
        shutil.move(pathname, old_path)
        shutil.move(rebuild_path, pathname)
        shutil.rmtree(old_path)
        return True
    except:
        LOG.warn("Cannot copy refreshed database to correct location: '%s'." %
            pathname)
        return False


def update(db, cache, datadir=None):
    if not datadir:
        datadir = APP_INSTALL_DESKTOP_PATH
    update_from_app_install_data(db, cache, datadir)
    update_from_var_lib_apt_lists(db, cache)
    # add db global meta-data
    LOG.debug("adding popcon_max_desktop '%s'" % popcon_max)
    db.set_metadata("popcon_max_desktop",
        xapian.sortable_serialise(float(popcon_max)))

def update_from_single_appstream_file(db, cache, filename):
    from lxml import etree

    tree = etree.parse(open(filename))
    root = tree.getroot()
    if not root.tag == "applications":
        LOG.error("failed to read '%s' expected Applications root tag" %
            filename)
        return
    for appinfo in root.iter("application"):
        parser = AppStreamXMLParser(appinfo, filename)
        index_app_info_from_parser(parser, db, cache)


def update_from_appstream_xml(db, cache, xmldir=None):
    if not xmldir:
        xmldir = softwarecenter.paths.APPSTREAM_XML_PATH
    context = GObject.main_context_default()

    if os.path.isfile(xmldir):
        update_from_single_appstream_file(db, cache, xmldir)
        return True

    for appstream_xml in glob(os.path.join(xmldir, "*.xml")):
        LOG.debug("processing %s" % appstream_xml)
        # process events
        while context.pending():
            context.iteration()
        update_from_single_appstream_file(db, cache, appstream_xml)
    return True


def update_from_app_install_data(db, cache, datadir=None):
    # index the desktop files in $datadir/desktop/*.desktop
    if not datadir:
        datadir = APP_INSTALL_DESKTOP_PATH
    context = GObject.main_context_default()
    for desktopf in glob(datadir + "/*.desktop"):
        LOG.debug("processing %s" % desktopf)
        # process events
        while context.pending():
            context.iteration()
        try:
            parser = DesktopConfigParser()
            parser.read(desktopf)
            index_app_info_from_parser(parser, db, cache)
        except Exception as e:
            # Print a warning, no error (Debian Bug #568941)
            LOG.debug("error processing: %s %s" % (desktopf, e))
            warning_text = _(
                "The file: '%s' could not be read correctly. The application "
                "associated with this file will not be included in the "
                "software catalog. Please consider raising a bug report "
                "for this issue with the maintainer of that "
                "application") % desktopf
            LOG.warning(warning_text)
    return True
"""