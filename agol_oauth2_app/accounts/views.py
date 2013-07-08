from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse


class LoginChoice(TemplateView):
    """
    A view that gives the user a choice of login type.
    """

    template_name = "accounts/LoginChoice.html"

    def get_context_data(self, **kwargs):
        context = super(LoginChoice, self).get_context_data(**kwargs)
        redirect_uri = settings.AGOL_OAUTH2_REDIRECT_URI
        context["next"] = self.request.GET.get("next",None)

        context["agoloauth2"] = "{0}/sharing/oauth2/authorize?client_id={1}&response_type=code&redirect_uri={2}".format(
            settings.AGOL_OAUTH2_PORTAL_URL,
            settings.AGOL_OAUTH2_APP_ID,
            redirect_uri
        )
        return context


class Logout(RedirectView):
    """
    A view that logs the user out of this system.  Once this occurs the user will have to log back in again,
    even if their AGOL token is still valid.
    """
    permanent = False

    def get_redirect_url(self, **kwargs):
        logout(self.request)
        return reverse('accounts_login_choice')


class Oauth2FromArcGISOnline(RedirectView):
    """
    This view takes in the redirect from the AGOL OAuth2 login, and decides if the user can be authenticated
    or if they should be redirected to the login choice page.
    """

    permanent = False

    def get_redirect_url(self, **kwargs):
        app = kwargs.get("app",None)
        code = self.request.GET.get("code",None)
        try:
            user = authenticate(oauth_code=code,app_name=app)
            login(self.request, user)
        except Exception as e:
            print e
            messages.info(self.request, "Sorry, but we could not authenticate your user in our system.")
            return reverse('accounts_login_choice')

        if code is not None and user is not None:
            #messages.info(self.request, "You have been logged in via ArcGIS Online as {0}".format(user.username))
            nextUrl = kwargs.get("next", None)
            if nextUrl is not None:
                url = nextUrl
            else:
                url = reverse('agol_app')
        else:
            messages.info(self.request, "Sorry, but we were unable to log you in via ArcGIS Online.")
            error = self.request.GET.get("error",None)
            error_description = self.request.GET.get("error_description",None)
            if error == "access_denied" and error_description == "The user denied your request.":
                messages.info(self.request, "It looks like you clicked cancel during the login process!")

            url = reverse('accounts_login_choice')
        return url


