# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test_500$', views.test_500, name='test_500'),
    url(r'^register/$', views.register, name='register'),
    url(r'^get_info/$', views.get_info, name='get_info'),
    url(r'^phone_login/$', views.phone_login, name='phone_login'),
    url(r'^phone_login_complete/$', views.phone_login_complete, name='phone_login_complete'),
]
