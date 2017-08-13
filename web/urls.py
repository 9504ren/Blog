# -*- coding:utf-8 -*-

from django.conf.urls import url
from .views import account,home


urlpatterns = [
    url(r'^login.html$', account.login),
    url(r'^register.html$', account.register),
    url(r'^check_code$', account.check),
    url(r'^logout.html$', account.logout),
    url(r'^updown.html', home.updown),
    url(r'^all-(?P<article_type_id>\d+).html', home.index),
    url(r'^detail/(?P<blog_id>\d+)-(?P<article_id>\d+).html',home.detail),
    # 忘记了url的匹配机制，是从前往后，匹配到了不会再向下匹配
    url(r'^', home.index),
]
