#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
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
from piston_mini_client.failhandlers import APIError

import piston_mini_client

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class ReviewRequest(PistonSerializable):
    _atts = ('machine', 'distro', 'version_os', 'version_uksc')


class RatingsAndReviewsAPI(PistonAPI):
    
    default_service_root = 'http://192.168.30.12/uksc/'
    default_content_type = 'application/x-www-form-urlencoded'

    @validate('review', ReviewRequest)
    @returns_json
    def submit_review(self,review):
        return self._post('pingbackmain/', data=review,scheme='http', content_type='application/json')


if __name__ == '__main__':
    wb = RatingsAndReviewsAPI()
    rdata = ReviewRequest()
    rdata.machine = '01010101010101'
    rdata.distro = 'ubuntu kylin'
    rdata.version_os = '14.10'
    rdata.version_uksc = '0.3.33'

    res = wb.submit_review(review=rdata)
    print res
    # decoded = json.loads(res)
    # print decoded