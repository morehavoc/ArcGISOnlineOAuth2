from django.conf.urls import patterns, url

from .views import LoginChoice
from .views import Oauth2FromArcGISOnline
from .views import Logout

urlpatterns = patterns('',
                       #Redirect from AGOL that specifies an app name
                       url(regex=r'^login/oauth/(?P<app>\w+)/$',
                           view=Oauth2FromArcGISOnline.as_view(),
                           name='accounts_login_oauth_app'),

                       #redriect from AGOL
                       url(regex=r'^login/oauth/$',
                           view=Oauth2FromArcGISOnline.as_view(),
                           name='accounts_login_oauth'),

                       #displays the login choice to the user.
                       url(regex=r'^login/$',
                           view=LoginChoice.as_view(),
                           name='accounts_login_choice'),

                       #logs the user out.
                       url(regex=r'^logout/$',
                           view=Logout.as_view(),
                           name='accounts_logout'),

                       #presents the user with a login screen for local authentication.
                       url(regex=r'^login/local/$',
                           view='django.contrib.auth.views.login',
                           name='accounts_login_local'),

                       )