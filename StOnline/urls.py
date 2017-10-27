# -*- coding: utf-8 -*-


from django.conf.urls import url,include
from django.contrib import admin
from django.views.static import serve

import users
from settings import MEDIA_ROOT,STATIC_ROOT


from django.views.generic import TemplateView
from users.views import LoginView,RegisterView,ActiveUserView,LogoutView,BeTeacher,Index
from organization.views import OrgView

import xadmin

urlpatterns = [
    url(r'^$', Index.as_view(), name="index"),
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),

    url('^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$',RegisterView.as_view(),name='register'),


    url(r'^captcha/',include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),


    url(r'^static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),




    url(r'^org/', include('organization.urls', namespace='org')),
    url(r'courses/', include('courses.urls', namespace='course')),
    url(r'^users/', include('users.urls', namespace='users')),







]
