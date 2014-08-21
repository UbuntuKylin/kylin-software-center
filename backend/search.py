#coding=utf-8
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

import locale
import logging
import os
import re
import string
import threading
import xapian
import apt
import time
import sys
from backend.ubuntu_sw import XapianValues


from gi.repository import GObject, Gio, GLib
from gettext import gettext as _
from xdg import BaseDirectory as xdg
LOG = logging.getLogger(__name__)

# xapian paths
XAPIAN_BASE_PATH = "/usr/share/ubuntu-kylin-software-center/data/"
XAPIAN_BASE_PATH_SOFTWARE_CENTER_AGENT = os.path.join(
    xdg.xdg_cache_home,
    "software-center",
    "software-center-agent.db")
XAPIAN_PATH = os.path.join(XAPIAN_BASE_PATH, "ukscsource_db")

# AXI
APT_XAPIAN_INDEX_BASE_PATH = "/var/lib/apt-xapian-index"
APT_XAPIAN_INDEX_DB_PATH = APT_XAPIAN_INDEX_BASE_PATH + "/index"
APT_XAPIAN_INDEX_UPDATE_STAMP_PATH = (APT_XAPIAN_INDEX_BASE_PATH +
                                      "/update-timestamp")
                                      
#ubuntu software-center paths
UTSC_PATH = "/var/cache/software-center/xapian"                   

def parse_axi_values_file(filename="/var/lib/apt-xapian-index/values"):
    """ parse the apt-xapian-index "values" file and provide the
    information in the self._axi_values dict
    """
    axi_values = {}
    if not os.path.exists(filename):
        return axi_values
    for raw_line in open(filename):
        line = string.split(raw_line, "#", 1)[0]
        if line.strip() == "":
            continue
        (key, value) = line.split()
        axi_values[key] = int(value)
    return axi_values


class SearchQuery(list):
    """ a list wrapper for a search query. it can take a search string
        or a list of search strings

        It provides __eq__ to easily compare two search query lists
    """
    def __init__(self, query_string_or_list):
        if query_string_or_list is None:
            pass
        # turn single queries into a single item list
        elif isinstance(query_string_or_list, xapian.Query):
            self.append(query_string_or_list)
        else:
            self.extend(query_string_or_list)

    def __eq__(self, other):
        # turn single queries into a single item list
        if isinstance(other, xapian.Query):
            other = [other]
        q1 = [str(q) for q in self]
        q2 = [str(q) for q in other]
        return q1 == q2

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "[%s]" % ",".join([str(q) for q in self])


class StoreDatabase(GObject.GObject):
    """thin abstraction for the xapian database with convenient functions"""

    # TRANSLATORS: List of "grey-listed" words separated with ";"
    # Do not translate this list directly. Instead,
    # provide a list of words in your language that people are likely
    # to include in a search but that should normally be ignored in
    # the search.
    SEARCH_GREYLIST_STR = _("app;application;package;program;programme;"
                            "suite;tool")

    # signal emitted
    __gsignals__ = {"reopen": (GObject.SIGNAL_RUN_FIRST,
                               GObject.TYPE_NONE,
                               ()),
                    "open": (GObject.SIGNAL_RUN_FIRST,
                             GObject.TYPE_NONE,
                             (GObject.TYPE_STRING,)),
                    }

    def __init__(self, pathname=None, cache=None):
        GObject.GObject.__init__(self)
        # initialize at creation time to avoid spurious AttributeError
        self._use_agent = False
        self._use_axi = False
        self._use_utsc = False

        if pathname is None:
            pathname = XAPIAN_PATH
        self._db_pathname = pathname
        locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")

        self._aptcache = cache
        self._additional_databases = []
        # the xapian values as read from /var/lib/apt-xapian-index/values
        self._axi_values = {}
        # we open one db per thread, thread names are reused eventually
        # so no memory leak
        self._db_per_thread = {}
        self._parser_per_thread = {}
        self._axi_stamp_monitor = None

    @property
    def xapiandb(self):
        """ returns a per thread db """
        thread_name = threading.current_thread().name
        if not thread_name in self._db_per_thread:
            self._db_per_thread[thread_name] = self._get_new_xapiandb()
        return self._db_per_thread[thread_name]


    @property
    def xapian_parser(self):
        """ returns a per thread query parser """
        thread_name = threading.current_thread().name
        if not thread_name in self._parser_per_thread:
            xapian_parser = self._get_new_xapian_parser()
            self._parser_per_thread[thread_name] = xapian_parser
        return self._parser_per_thread[thread_name]

    def _get_new_xapiandb(self):
        xapiandb = xapian.Database(self._db_pathname)
        if self._use_axi:
            try:
                axi = xapian.Database(
                    APT_XAPIAN_INDEX_DB_PATH)
                xapiandb.add_database(axi)
            except Exception as e:
                logging.warn("failed to add apt-xapian-index db %s" % e)
        if (self._use_agent and
                os.path.exists(XAPIAN_BASE_PATH_SOFTWARE_CENTER_AGENT)):
            try:
                sca = xapian.Database(XAPIAN_BASE_PATH_SOFTWARE_CENTER_AGENT)
                xapiandb.add_database(sca)
            except Exception as e:
                #logging.warn("failed to add sca db %s" % e)
                pass
        if self._use_utsc:
            try:
                utsc_xapiandb = xapian.Database(UTSC_PATH)
                xapiandb.add_database(utsc_xapiandb)
            except Exception as e:
                #logging.warn("failed to add utsc_xapiandb db %s" % e)
                pass
                
        for db in self._additional_databases:
            xapiandb.add_database(db)
        return xapiandb

    def _get_new_xapian_parser(self):
        xapian_parser = xapian.QueryParser()
        xapian_parser.set_database(self.xapiandb)
        xapian_parser.add_boolean_prefix("pkg", "XP")
        xapian_parser.add_boolean_prefix("pkg", "AP")
        xapian_parser.add_boolean_prefix("mime", "AM")
        xapian_parser.add_boolean_prefix("section", "XS")
        xapian_parser.add_boolean_prefix("origin", "XOC")
        xapian_parser.add_prefix("pkg_wildcard", "XP")
        xapian_parser.add_prefix("pkg_wildcard", "XPM")
        xapian_parser.add_prefix("pkg_wildcard", "AP")
        xapian_parser.add_prefix("pkg_wildcard", "APM")
        xapian_parser.set_default_op(xapian.Query.OP_AND)
        return xapian_parser

    def open(self, pathname=None, use_axi=True, use_agent=True,use_utsc=True):
        """ open the database """
        LOG.debug("open() database: path=%s use_axi=%s "
                          "use_agent=%s" % (pathname, use_axi, use_agent))
        if pathname:
            self._db_pathname = pathname
        # clean existing DBs on open
        self._db_per_thread = {}
        self._parser_per_thread = {}
        # add the apt-xapian-database for here (we don't do this
        # for now as we do not have a good way to integrate non-apps
        # with the UI)
        self.nr_databases = 0
        self._use_axi = use_axi
        self._axi_values = {}
        self._use_agent = use_agent
        self._use_utsc = use_utsc
        if use_axi:
            if self._axi_stamp_monitor:
                self._axi_stamp_monitor.disconnect_by_func(
                    self._on_axi_stamp_changed)
            self._axi_values = parse_axi_values_file()
            self.nr_databases += 1
            # mvo: we could monitor changes in
            #       softwarecenter.paths.APT_XAPIAN_INDEX_DB_PATH here too
            #       as its a text file that points to the current DB
            #       *if* we do that, we need to change the event == ATTRIBUTE
            #       change in _on_axi_stamp_changed too
            self._axi_stamp = Gio.File.new_for_path(
                APT_XAPIAN_INDEX_UPDATE_STAMP_PATH)
            self._timeout_id = None
            self._axi_stamp_monitor = self._axi_stamp.monitor_file(0, None)
            self._axi_stamp_monitor.connect(
                "changed", self._on_axi_stamp_changed)
        if use_agent:
            self.nr_databases += 1
        if use_utsc:
            self.nr_databases += 1
        # additional dbs
        for db in self._additional_databases:
            self.nr_databases += 1
        self.emit("open", self._db_pathname)

    def _on_axi_stamp_changed(self, monitor, afile, otherfile, event):
        # we only care about the utime() update from update-a-x-i
        if not event == Gio.FileMonitorEvent.ATTRIBUTE_CHANGED:
            return
        LOG.debug("afile '%s' changed" % afile)
        if self._timeout_id:
            GLib.source_remove(self._timeout_id)
            self._timeout_id = None
        self._timeout_id = GLib.timeout_add(500, self.reopen)

    def add_database(self, database):
        self._additional_databases.append(database)
        self.xapiandb.add_database(database)
        self.reopen()


    def reopen(self):
        """ reopen the database """
        LOG.debug("reopen() database")
        self.open(use_axi=self._use_axi, use_agent=self._use_agent)
        self.emit("reopen")


    def get_query_for_pkgnames(self, pkgnames):
        """ return a xapian query that matches exactly the list of pkgnames """
        enquire = xapian.Enquire(self.xapiandb)
        query = xapian.Query()
        for pkgname in pkgnames:
            # even on the raspberry pi this query is super quick (~0.003s)
            with ExecutionTime("de-dup query_for_pkgnames"):
                tmp_query = xapian.Query("AP" + pkgname)
                enquire.set_query(tmp_query)
                result = enquire.get_mset(0, 1)
            # see bug #1043159, we need to ensure that we de-duplicate
            # when there is a pkg and a app (e.g. from the s-c-agent) in the db
            if len(result) == 1:
                query = xapian.Query(xapian.Query.OP_OR,
                                     query,
                                     xapian.Query("AP" + pkgname))
            else:
                query = xapian.Query(xapian.Query.OP_OR,
                                     query,
                                     xapian.Query("XP" + pkgname))
        return query

    def get_query_list_from_search_entry(self, search_term,
        category_query=None):
        """ get xapian.Query from a search term string and a limit the
            search to the given category
        """
        def _add_category_to_query(query):
            """ helper that adds the current category to the query"""
            if not category_query:
                return query
            return xapian.Query(xapian.Query.OP_AND,
                                category_query,
                                query)
        # empty query returns a query that matches nothing (for performance
        # reasons)
        if search_term == "" and category_query is None:
            return SearchQuery(xapian.Query())
        # we cheat and return a match-all query for single letter searches
        if len(search_term) < 2:
            return SearchQuery(_add_category_to_query(xapian.Query("")))

        # check if there is a ":" in the search, if so, it means the user
        # is using a xapian prefix like "pkg:" or "mime:" and in this case
        # we do not want to alter the search term (as application is in the
        # greylist but a common mime-type prefix)
        if not ":" in search_term:
            # filter query by greylist (to avoid overly generic search terms)
            orig_search_term = search_term
            for item in self.SEARCH_GREYLIST_STR.split(";"):
                (search_term, n) = re.subn('\\b%s\\b' % item, '', search_term)
                if n:
                    LOG.debug("greylist changed search term: '%s'" %
                        search_term)
        # restore query if it was just greylist words
        if search_term == '':
            LOG.debug("grey-list replaced all terms, restoring")
            search_term = orig_search_term
        # we have to strip the leading and trailing whitespaces to avoid having
        # different results for e.g. 'font ' and 'font' (LP: #506419)
        search_term = search_term.strip()
        # get a pkg query
        if "," in search_term:
            pkg_query = self.get_query_for_pkgnames(search_term.split(","))
        else:
            pkg_query = xapian.Query()
            for term in search_term.split():
                pkg_query = xapian.Query(xapian.Query.OP_OR,
                                         xapian.Query("XP" + term),
                                         pkg_query)
        pkg_query = _add_category_to_query(pkg_query)

        # get a search query
        if not ':' in search_term:  # ie, not a mimetype query
            # we need this to work around xapian oddness
            search_term = search_term.replace('-', '_')
        fuzzy_query = self.xapian_parser.parse_query(search_term,
                                           xapian.QueryParser.FLAG_PARTIAL |
                                           xapian.QueryParser.FLAG_BOOLEAN)
        # if the query size goes out of hand, omit the FLAG_PARTIAL
        # (LP: #634449)
        if fuzzy_query.get_length() > 1000:
            fuzzy_query = self.xapian_parser.parse_query(search_term,
                                            xapian.QueryParser.FLAG_BOOLEAN)
        # now add categories
        fuzzy_query = _add_category_to_query(fuzzy_query)
        return SearchQuery([pkg_query, fuzzy_query])


    def __len__(self):
        """return the doc count of the database"""
        return self.xapiandb.get_doccount()

    def __iter__(self):
        """ support iterating over the documents """
        for it in self.xapiandb.postlist(""):
            doc = self.xapiandb.get_document(it.docid)
            yield doc


class ExecutionTime(object):
    """
    Helper that can be used in with statements to have a simple
    measure of the timing of a particular block of code, e.g.
    with ExecutinTime("db flush"):
        db.flush()
    """
    def __init__(self, info="", with_traceback=False,
                 suppress_less_than_n_seconds=0.1):
        self.info = info
        self.with_traceback = with_traceback
        self.suppress_less_than_n_seconds = suppress_less_than_n_seconds

    def __enter__(self):
        self.now = time.time()

    def __exit__(self, type, value, stack):
        time_spend = time.time() - self.now
        if time_spend < self.suppress_less_than_n_seconds:
            return
        logger = logging.getLogger("softwarecenter.performance")
        logger.debug("%s: %s" % (self.info, time_spend))
        if self.with_traceback:
            log_traceback("populate model from query: '%s' (threaded: %s)")

def log_traceback(info):
    """
    Helper that can be used as a debug helper to show what called
    the code at this place. Logs to softwarecenter.traceback
    """
    logger = logging.getLogger("softwarecenter.traceback")
    logger.debug("%s: %s" % (info, "".join(traceback.format_stack())))

class Search:
    db = ''
    def __init__(self):
        self.db = StoreDatabase(XAPIAN_PATH, apt.Cache())
        try:
            self.db.xapiandb
        except:
            print "failed to add db"
            LOG.exception("failed to add db")
        self.db.open()
        
    def search_software(self, keyword):
        """search interface"""
        
#*****************************************************************************
        try:
        
            from mmseg.search import seg_txt_search,seg_txt_2_dict
            query_string = str(keyword)
            enquire = xapian.Enquire(self.db.xapiandb)
            
            query_list = []
            for word, value in seg_txt_2_dict(query_string).iteritems():
                query = xapian.Query(word, value)
#               print word,value
                query_list.append(query)
            if len(query_list) != 1:
                query = xapian.Query(xapian.Query.OP_AND, query_list)
            else:
                query = query_list[0]
#            print "*** Useing Chinese Segmentation method MMSEG to segment the input keywords ***"

#*********************************************************************************
        except:   

            Info = """
*********************************************************
There is no Chinese Segmentation method MMSEG in
your system.For better useing of ubuntu-kylin-software-center,
please install chinese Segmentation method MMSEG .
*********************************************************
"""
            print Info
            query_string = self.db.get_query_list_from_search_entry(str(keyword))
            enquire = xapian.Enquire(self.db.xapiandb)
            query = query_string[1]

#            enquire = xapian.Enquire(self.db.xapiandb)
#            qp = xapian.QueryParser()
#            qp.set_database(self.db.xapiandb)

#            query = qp.parse_query(str(keyword))
#            print "Parsed query is: %s"% str(query)

        enquire.set_query(query)
        matches = enquire.get_mset(0, len(self.db))
#        print "res len=",len(self.db),len(matches)
        pkgnamelist = []
        for m in matches:
            doc = m.document
#            print m.docid
#            print '************************************'
            pkgname = doc.get_value(XapianValues.PKGNAME)

            if not pkgname:
                pkgname = doc.get_data()

            if pkgname:
                #check weather exist in the list
                try:
                    index = pkgnamelist.index(pkgname)
                #not exist will raise ValueError
                except ValueError:
                    pkgnamelist.append(pkgname)
        
                    
#        print pkgnamelist        
        return pkgnamelist


#import axi

if __name__ == "__main__":
    
    s = Search()
#    uksc_xapiandb=s.db._get_new_xapiandb()
    res = s.search_software("ubuntu-kylin-software-center")

