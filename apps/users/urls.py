#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from users.forms import UploadCourseImgForm
from .views import UserInfoView, UploadImageView, UpdatePwdView, \
    SendMailCodeView, UpdateEmailView, MyCourseView, \
    MyFavOrgView, MyFavTeacherView, MyFavCourseView,\
    MyMessageView,BeTeacher,Publish,SendMsg, UploadCourseImgView

urlpatterns = [

    url('^send_msg/$', SendMsg.as_view(), name='send_msg'),

    url('^to_be_teacher/$', BeTeacher.as_view(), name='be_teacher'),

    url(r'^publish/$', Publish.as_view(), name='user_publish'),

    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),

    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),

    url(r'^course_image/upload/(?P<course_id>\d+)/$', UploadCourseImgView.as_view(), name='course_image_upload'),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 用户中心修改邮箱
    url(r'^sendemail_code/$', SendMailCodeView.as_view(), name='sendemail_code'),

    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),

    # 我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),

    # 我收藏的授课讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),

    # 我收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),

    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),

]
