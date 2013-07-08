import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist

from .models import user_profile


class AGOLApplicationLogin(object):
    """
    Basic class to support OAUTH2 login via the application's credentials.
    """

    def authenticate(self):
        data = {}
        data['client_id'] = settings.AGOL_OAUTH2_APP_ID
        data['client_secret'] = settings.AGOL_OAUTH2_SECRET
        data['grant_type'] = 'client_credentials'

        postUrl = settings.AGOL_OAUTH2_PORTAL_URL+'/sharing/oauth2/token'
        r = requests.post(postUrl, data=data)
        # if an error state is returned (not 200) then raise that error here.
        r.raise_for_status()
        response = r.json()
        print response
        if 'error' in response:
            #This means the user was not authenticated via AGOL, so we need to display an error.
            return None
        return response


class EagleModelBackend(ModelBackend):
    """
    Modified Backend to support authenticating the user via AGOL after the application has authenticated them
    using a regular Django ModelBackend
    """

    def authenticate(self, username=None, password=None, **kwargs):
        user = super(EagleModelBackend, self).authenticate(username, password, **kwargs)
        if user is None:
            return user

        #the user is authenticated, so now we want to authenticate the application
        app = AGOLApplicationLogin()
        newToken = app.authenticate()
        try:
            user.user_profile.agol_token = newToken['access_token']
            user.user_profile.agol_user = False
            user.user_profile.agol_expires_at = newToken['expires_in']
            user.user_profile.save()
        except ObjectDoesNotExist:
            up = user_profile(user=user)
            up.agol_token = newToken['access_token']
            up.agol_user = False
            user.user_profile.agol_expires_at = newToken['expires_in']
            up.save()
            user.save()
        return user


class AGOLBackend(object):
    """
    Authenticates a user via AGOL, this user does not yet have to have a record in the local user database, although
    that user will have a record after they have successfully authenticated.
    The workflow looks something like this:
    1 - The user click "login with AGOL"
    2 - The user is redirected to an AGOL login page, hosted by AGOL, where we identify the application via client_id
    3 - After the user has been authenticated, AGOL redirects the user back to a page on this site with an OAUTH code
    4 - The app ends up here trying to authenticate the user
    5 - This process makes a call to the token endpoint of AGOL with the client_id, client_secret, and code from the
        redirect.
    6 - AGOL responds with an access_token, refresh_token and an expire date.
    7 - All of these tokens are saved in a user_profile table.  If the user is not already in the system
        then a new account is created using their AGOL username, with an invalid password.
    8 - The user is redirected to a page that actually does something.
    """

    def authenticate(self, oauth_code=None, app_name=None):
        #take the oauth_code, and make a call to the arcgis rest endpoints to turn that into
        # a token, and a refresh token, and save that into the users profile.
        #Then add this backend to the possible authentication backends, and
        #call this from accounts.views.Oauth2FromArcGISOnline.get_redirect_url
        #to authenticate the user using the code returned via the callback.

        #build the request to call to AGOL to get tokens in place of the oauth code
        data = {}
        data['client_id'] = settings.AGOL_OAUTH2_APP_ID
        data['client_secret'] = settings.AGOL_OAUTH2_SECRET
        data['grant_type'] = 'authorization_code'
        data['code'] = oauth_code
        if app_name:
            data['redirect_uri'] = settings.AGOL_OAUTH2_REDIRECT_URI + "/" + app_name + "/"
        else:
            data['redirect_uri'] = settings.AGOL_OAUTH2_REDIRECT_URI

        postUrl = settings.AGOL_OAUTH2_PORTAL_URL+'/sharing/oauth2/token'
        r = requests.post(postUrl,data=data)
        r.raise_for_status()
        response =  r.json()
        if response.has_key('error') == True:
            # the user was not authenticated correctly for some reason
            return None

        #try to get the user based on the username returned in the response
        username = response.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                try:
                    user.user_profile.agol_user = True
                    user.user_profile.agol_token = response.get('access_token')
                    user.user_profile.agol_refresh_token = response.get('refresh_token')
                    user.user_profile.agol_expires_at = response.get('expires_in')
                    user.user_profile.save()
                    user.save()
                except ObjectDoesNotExist:
                    up = user_profile(user=user)
                    up.agol_user = True
                    up.agol_token = response.get('access_token')
                    up.agol_refresh_token = response.get('refresh_token')
                    up.agol_expires_at = response.get('expires_in')
                    up.save()
                    user.save()
            except User.DoesNotExist:
                #the user does not exist, we will now need to create the user.
                #return None
                user = User(username=username,  password='a random string')
                user.is_staff = False
                user.is_superuser = False
                user.save()
                up = user_profile(user=user)
                up.agol_user = True
                up.agol_token = response.get('access_token')
                up.agol_refresh_token = response.get('refresh_token')
                up.agol_expires_at = response.get('expires_in')
                up.save()
                user.save()
            return user
        return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None