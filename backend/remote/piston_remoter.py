#!/usr/bin/python3
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


#from urllib.parse import quote_plus
import urllib.request, urllib.parse, urllib.error
from urllib.parse import quote_plus
from piston_mini_client import (
    PistonAPI,
    PistonResponseObject,
    PistonSerializable,
    returns,
    returns_json,
    returns_list_of,
    auth,
    )
from models.enums import UBUNTUKYLIN_SERVER
import time
from models.globals import Globals
from piston_mini_client.validators import validate_pattern, validate
from piston_mini_client import APIError
import httplib2
import json
import sys



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


class RatinsUKRequest(PistonSerializable):
    _atts = ('app_name', 'rating', 'user', 'user_display')


class ReviewUKRequest(PistonSerializable):
    _atts = ('app_name', 'content', 'distroseries', 'language', 'user', 'user_display')


class PingbackmainRequest(PistonSerializable):
    _atts = ('machine', 'distro', 'version_os', 'version_uksc')


class PingbackappRequest(PistonSerializable):
    _atts = ('app_name', 'machine', 'isrcm', 'user')

class AppTransinfoUKRequest(PistonSerializable):
    _atts = ('app_name','type_appname', 'type_summary', 'type_description', 'original_appname', 'original_summary', 'original_description', 'transl_appname', 'transl_summary', 'transl_description', 'user', 'user_display')


class ADDUSERRequest(PistonSerializable):
    _atts = ('username','password','email','identity')

class Applogin(PistonSerializable):
    _atts = ('username','password')

class Rsetpassword(PistonSerializable):
    _atts = ('username','password')

class Recoverpassword(PistonSerializable):
    _atts = ('username','email')
class Changeidentity(PistonSerializable):
    _atts = ('username','identity')

class PistonRemoter(PistonAPI):

    default_service_observe = 'observe'
    default_service_forecast3d = 'forecast3d'
    default_content_type = 'application/x-www-form-urlencoded'
    default_service_root = UBUNTUKYLIN_SERVER
    default_timeout = 2

    #
    # 函数：获取所有评分接口
    #
    @returns_json
    def get_all_ratings(self):
        gets = self._get("getallratings", scheme="http")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        if (Globals.DEBUG_SWITCH):
            print("get_all_ratings")
        return gets

    #
    # 函数：获取用户评分接口
    #
    @returns_json
    def get_user_ratings(self,user_name,app_name):
        get_ratings =self._get('getuserratings/?user_name=%s;app_name=%s' % (user_name,app_name),scheme="http")
        if (isinstance(get_ratings,bytes)):
            get_ratings = get_ratings.decode(encoding='utf-8')
        if (Globals.DEBUG_SWITCH):
            print(get_ratings)
        return get_ratings

    #
    # 函数：获取下载次数统计
    #
    @returns_json
    def get_Amount_Downloads(self,app_name):
        get_Downcont=self._get('downloadcontrol/?app_name=%s' % (app_name),scheme="http")
        if (isinstance(get_Downcont,bytes)):
            get_Downcont = get_Downcont.decode(encoding='utf-8')
        if (Globals.DEBUG_SWITCH):
            print(get_Downcont)
        return get_Downcont

    #
    # 函数：获取软件评论
    #
    @returns_list_of(ReviewUK)
    def get_reviews(self, app, start, range_):
        getreviews = self._get('getreviews/?app=%s;start=%s;range=%s' % (app, start, range_), scheme="http")
        if (isinstance(getreviews,bytes)):
            getreviews = getreviews.decode(encoding='utf-8')
        return getreviews

    #
    # 函数：获取新的评论
    #
    @returns_list_of(ReviewUK)
    def get_newest_review(self, app):
        start = 0
        range_ = 1
        gets = self._get('getreviews/?app=%s;start=%s;range=%s' % (app, start, range_), scheme="http")
        if (Globals.DEBUG_SWITCH):
            print("get_newest_review")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：提交软件启动记录
    #
    @returns_json
    def submit_pingback_main(self, machine, distro, version_os, version_uksc):
        postdata = PingbackmainRequest()
        postdata.machine = machine
        postdata.distro = distro
        postdata.version_os = version_os
        postdata.version_uksc = version_uksc
        gets = self._post('pingbackmain/', data=postdata, scheme='http', content_type='application/json')
        if (Globals.DEBUG_SWITCH):
            print("submit_pingback_main")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：提交软件安装记录
    #
    @returns_json
    def submit_pingback_app(self, app_name, machine, isrcm, user):
        postdata = PingbackappRequest()
        postdata.app_name = app_name
        postdata.machine = machine
        postdata.isrcm = isrcm
        if(not user):
            user = "User_is_Null"
        postdata.user = user
        gets = self._post('pingbackapp20141014/', data=postdata, scheme='http', content_type='application/json')
        if (Globals.DEBUG_SWITCH):
            print("submit_pingback_app")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：获取所有软件分类
    #
    @returns_json
    def get_all_categories(self):
        gets = self._get("getallcategories", scheme="http")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        if (Globals.DEBUG_SWITCH):
            print("get_all_categories")
        return gets

    #
    # 函数：获取排名和推荐
    #
    @returns_json
    def get_all_rank_and_recommend(self):
        gets = self._get("getallrankandrecommend", scheme='http')
        if (Globals.DEBUG_SWITCH):
            print("get_all_rank_and_recommend")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：获取新应用的信息
    #
    @returns_json
    def get_newer_application_info(self, last_update_date):
        gets = self._get('getnewerapplicationinfo/?modify_time=%s' % last_update_date, scheme="http")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        if (Globals.DEBUG_SWITCH):
            print("get_newer_application_info")
        return gets

    #
    # 函数：获取新应用的图标
    #
    @returns_json
    def get_newer_application_icon(self, last_update_date):
        gets = self._get('getnewericon/?modify_time=%s' % last_update_date, scheme="http")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        if (Globals.DEBUG_SWITCH):
            print("get_newer_application_icon")
        return gets

    #
    # 函数：获取新应用广告
    #
    @returns_json
    def get_newer_application_ads(self, last_update_date):
        gets = self._get('getnewads/?modify_time=%s' % last_update_date, scheme="http")
        if (isinstance(gets, bytes)):
            gets = gets.decode(encoding='utf-8')
        if (Globals.DEBUG_SWITCH):
            print("get_newer_application_icon")
        return gets

    #
    # 函数：获取新应用的截图
    #
    @returns_json
    def get_newer_application_screenshots(self, last_update_date):
        gets = self._get ('getsmallscreenshots/?modify_time=%s' % last_update_date, scheme="http")

        if (isinstance(gets, bytes)):
            gets = gets.decode(encoding='utf-8')
        if (Globals.DEBUG_SWITCH):
            print("get_newer_application_screenshots")
        return gets

    #
    # 函数：xapian数据库所有应用更新
    #
    @returns_json
    def allapp_forxapianupdate(self):
        gets = self._get('allappforxapianupdate/?', scheme="http")
        if (Globals.DEBUG_SWITCH):
            print("allapp_forxapianupdate")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：xiapian数据库新增应用更新
    #
    @returns_json
    def newerapp_for_xapianupdate(self, the_latest_update_time):
        gets = self._get('newerappforxapianupdate/?update_datetime=%s' % the_latest_update_time, scheme="http")
        if (Globals.DEBUG_SWITCH):
            print("newerapp_for_xapianupdate")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：获取用户安装列表
    #
    @returns_json
    def get_user_applist(self, user):
        gets = self._get('getapplist/?user=%s' % user, scheme="http")
        if (Globals.DEBUG_SWITCH):
            print("get_user_applist")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：获取用户翻译列表
    #
    @returns_json
    def get_user_transapplist(self, user):
        gets = self._get('getusertranslation/?user=%s' % user, scheme="http")
        if (Globals.DEBUG_SWITCH):
            print("get_user_transapplist")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：创建用户
    #
    @returns_json
    def submit_add_user(self,username,password,email,identity):
        postdata = ADDUSERRequest()
        postdata.username = username
        postdata.password = password
        postdata.email = email
        postdata.identity = identity
        gets = self._post('register/', data=postdata, scheme='http', content_type='application/json')
        if (Globals.DEBUG_SWITCH):
            print("submit_add_user")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：重置密码
    #
    @returns_json
    def rset_user_password(self, username ,newpwd):
        #postdata = Rsetpassword()
        #postdata.username = username
        #postdata.password = password
        gets = self._get('changepwd/?username=%s;newpwd=%s;' % (username, newpwd), scheme='http')
        if (Globals.DEBUG_SWITCH):
            print("rset_user_password")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：找回密码
    #
    @returns_json
    def recover_user_password(self, username ,email, newpwd):
        #postdata = Reecoverpassword()
        #postdata.username = username
        #postdata.email = email
        gets = self._get('retrievepwd/?username=%s;email=%s;newpwd=%s;' % (username, email, newpwd), scheme="http")
        if (Globals.DEBUG_SWITCH):
            print("recover_user_password")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：改变用户身份
    #
    @returns_json
    def change_user_identity(self, username ,identity):
        #postdata = Changeidentity()
        #postdata.username = username
        #postdata.identity = identity
        gets = self._get('changeidentity/?username=%s;identity=%s;' % (username ,identity), scheme="http")
        if (Globals.DEBUG_SWITCH):
            print("change_user_identity")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    @returns_json
    def log_in_appinfo(self,username,password):
        postdata = Applogin()
        postdata.username = username
        postdata.password = password
        gets = self._post('login/', data=postdata, scheme='http', content_type='application/json')
        if (Globals.DEBUG_SWITCH):
            print("log_in_appinfo")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets



#class PistonRemoterAuth(PistonAPI):

#    default_service_observe = 'observe'
#    default_service_forecast3d = 'forecast3d'
#    default_content_type = 'application/x-www-form-urlencoded'
#    default_service_root = UBUNTUKYLIN_SERVER

    #
    # 函数：提交应用评论
    #
    @returns_json
    def submit_review(self, app_name, content, distroseries, language, user, user_display):
        postdata = ReviewUKRequest()
        postdata.app_name = app_name
        postdata.content = content
        postdata.distroseries = distroseries
        postdata.language = language
        postdata.user = user
        postdata.user_display = user_display
        gets = self._post('submitreview20141124/', data=postdata, scheme='http', content_type='application/json')
        if (Globals.DEBUG_SWITCH):
            print("submit_review")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：提交翻译信息
    #
    @returns_json
    def submit_translate_appinfo(self, appname,type_appname, type_summary, type_description, orig_appname, orig_summary, orig_description, trans_appname, trans_summary, trans_description, user, user_display):
        postdata = AppTransinfoUKRequest()
        postdata.app_name = appname
        #print postdata.app_name
        postdata.type_appname = type_appname
        #print postdata.type_appname
        postdata.type_summary = type_summary
        #print postdata.type_summary
        postdata.type_description = type_description
        #print postdata.type_description
        postdata.original_appname = orig_appname
        #print postdata.original_appname
        postdata.original_summary = orig_summary
        #print postdata.original_summary
        postdata.original_description = orig_description
        #print postdata.original_description,type(orig_description)
        postdata.transl_appname = trans_appname
        #print postdata.transl_appname
        postdata.transl_summary = trans_summary
        #print postdata.transl_summary
        postdata.transl_description = trans_description
        #print postdata.transl_description
        postdata.user = user
        #print postdata.user
        postdata.user_display = user_display
        #print postdata.user_display
        gets = self._post('submittranslation/', data=postdata, scheme='http', content_type='application/json')
        if (Globals.DEBUG_SWITCH):
            print("submit_translate_appinfo")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets

    #
    # 函数：提交应用评分
    #
    @returns_json
    def submit_rating(self, app_name, rating, user, user_display):
        postdata = RatinsUKRequest()
        postdata.app_name = app_name
        postdata.rating = rating
        postdata.user = user
        postdata.user_display = user_display
        gets = self._post('submitrating0923/', data=postdata, scheme='http', content_type='application/json')
        if (Globals.DEBUG_SWITCH):
            print("submit_rating")
        if (isinstance(gets,bytes)):
            gets = gets.decode(encoding='utf-8')
        return gets


if __name__ == '__main__':
    from backend.ubuntusso import *
    from utils.machine import *
    # from
    sso = get_ubuntu_sso_backend()
    token = sso.get_oauth_token_and_verify_sync()
    authorizer = auth.OAuthAuthorizer(token["token"], token["token_secret"], token["consumer_key"], token["consumer_secret"])
    ss = PistonRemoterAuth(auth=authorizer)
    res = ss.submit_review('gimp', 'main', get_distro_info()[2], get_language(),'shine','shine')
    if (Globals.DEBUG_SWITCH):
        print(res)
        print((type(res)))
    # s = PistonRemoter(service_root="http://192.168.30.12/uksc/")
    # res = s.get_all_categories()
    # res = s.get_all_rank_and_recommend()
    # print res
    # res = s.submit_pingback_main("123123","ubuntutu","1414","0.99")
    # print res
    # res = s.submit_pingback_app("pyracerz","jioqjwfiqwf","True")
    # print res
    # res = s.get_newer_application_info('2014-07-23')
    # print res
    # reslist = s._get("getallratings", scheme="http")
    # reslist = s.get_all_ratings()
    # print len(reslist)
    # import json
    # decoded = json.loads(reslist)
    # print len(decoded)
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
