"""Urls for emg_intra.ged"""
from django.conf.urls.defaults import *

urlpatterns = patterns('emencia.django.ged.views',
                       url(r'^(?P<path>[-\/\w]+)$', 'view_browsing',
                           name='ged_path_browsing'),
                       url(r'^$', 'view_browsing', {'path': '/'},
                           name='ged_root_browsing'),                       
                       )
