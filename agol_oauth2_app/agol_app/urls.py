from django.conf.urls import patterns, url
from .views import AGOLApp

urlpatterns = patterns('',

                       #loads the root directory as the html/js application
                       url(regex=r'^$',
                           view=AGOLApp.as_view(),
                           name='agol_app'),

                       )