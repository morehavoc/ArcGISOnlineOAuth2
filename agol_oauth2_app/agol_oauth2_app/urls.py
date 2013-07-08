from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import accounts.urls
import agol_app.urls

urlpatterns = patterns('',

    #url(r'^admin/', include(admin.site.urls)),

    #load the URLS from the accounts app
    url(r'^accounts/', include(accounts.urls.urlpatterns)),

    #load the urls from the agol_app (the html/js app).
    url(r'^$', include(agol_app.urls.urlpatterns)),
)
