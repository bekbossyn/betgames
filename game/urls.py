# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^info/$', views.info, name='info'),
    url(r'^update/$', views.update, name='update'),
    url(r'^update_token/$', views.update_token, name='update_token'),
    url(r'^update_sound/$', views.update_sound, name='update_sound'),
    url(r'^test_push/$', views.test_push, name='test_push'),
    url(r'^update_sound_name/$', views.update_sound_name, name='update_sound_name'),
    url(r'^update_push/$', views.update_push, name='update_push'),
    url(r'^send_feedback/$', views.send_feedback, name='send_feedback'),
    url(r'^reset/$', views.reset, name='reset'),
]
