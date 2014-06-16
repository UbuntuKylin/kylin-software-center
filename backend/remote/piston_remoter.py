#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE

# Copyright (C) 2013 National University of Defense Technology(NUDT) & Kylin Ltd

# Author:
#     Shine Huang<shenghuang@ubuntukylin.com>
# Maintainer:
#     Shine Huang<shenghuang@ubuntukylin.com>

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


from urllib import quote_plus
from piston_mini_client import (
    PistonAPI,
    PistonResponseObject,
    PistonSerializable,
    returns,
    returns_json,
    returns_list_of,
    )
from piston_mini_client.validators import validate_pattern, validate
from piston_mini_client import APIError
import httplib2


class ReviewUK(PistonResponseObject):
    """
    id
    content
    date
    user_display
    user
    aid: {
        id
        review_total
    }
    """
    pass

class PistonRemoter(PistonAPI):

    default_service_observe = 'observe'
    default_service_forecast3d = 'forecast3d'
    default_content_type = 'application/x-www-form-urlencoded'

    @returns_json
    def get_all_ratings(self):
        return self._get("getallratings", scheme="http")

    @returns_list_of(ReviewUK)
    def get_reviews(self, app, start, range_):
        # start = (page - 1) * 10
        # range_ = 10
        return self._get('getreviews/?app=%s;start=%s;range=%s' % (app, start, range_), scheme="http")

    @returns_list_of(ReviewUK)
    def get_newest_review(self, app):
        start = 0
        range_ = 1
        return self._get('getreviews/?app=%s;start=%s;range=%s' % (app, start, range_), scheme="http")


if __name__ == '__main__':
    s = PistonRemoter(service_root="http://service.ubuntukylin.com:8001/uksc/")
    reslist = s._get("getallratings", scheme="http")
    #
    # try:
    # res = s.get_all_ratings()
    # print res[0]
    # print "res : ",res[0]['app_name']
    # print "res : ",res[0]['rating_avg']
    # print "res : ",res[0]['rating_total']

    # res = s.get_reviews('gedit', 2)


    # res = s.get_newest_review('gedit')
    # for r in res:
    #     print r.user
    #     print r.user_display
    #     print r.content
    #     print r.date
    #     print r.aid['review_total']
    #     print '\n'


    # except ValueError as e:
    #     print "failed to parse '%s'" % e
    # except APIError as e:
    #     print e
    # except httplib2.ServerNotFoundError:
    #     s._offline_mode = True
    #     res = s.get_all_ratings('hehehe')
    # except:
    #     print "other except"


    # s2 = PistonRemoter(service_root="http://reviews.ubuntu.com/reviews/api/1.0")
    # res = s2.get_reviewss("gedit",language="zh_CN",page=1)
    # Review.from_piston_mini_client(res[0])

    # reviews = []
    # for r in res:
    #     review = Review.from_piston_mini_client(r)
    #     print review.review_text

        # print review.reviewer_username
        # print review.reviewer_displayname
        # print review.summary
        # print review.rating
        # print review.date_created
        # print review.review_text

        # reviews.append(review)