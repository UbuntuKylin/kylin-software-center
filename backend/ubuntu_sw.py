# Copyright (C) 2009 Canonical
#
# Authors:
#  Michael Vogt
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

    def __cmp__(self, other):
        # first compare version, high version number first
        vc = upstream_version_compare(self.version, other.version)
        if vc != 0:
            return vc
        # then wilson score
        uc = cmp(wilson_score(self.usefulness_favorable,
                              self.usefulness_total),
                 wilson_score(other.usefulness_favorable,
                              other.usefulness_total))
        if uc != 0:
            return uc
        # last is date
        t1 = datetime.datetime.strptime(self.date_created, '%Y-%m-%d %H:%M:%S')
        t2 = datetime.datetime.strptime(other.date_created,
            '%Y-%m-%d %H:%M:%S')
        return cmp(t1, t2)

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
