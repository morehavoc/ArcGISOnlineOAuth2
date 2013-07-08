from django.views.generic import TemplateView
from django.conf import settings

from braces.views import LoginRequiredMixin


class AGOLApp(LoginRequiredMixin, TemplateView):
    """
    This view loads the template that contains the HTML/JS application.  Basically if the user is authenticated
    (the LoginRequiredMixin) then this view will return the proper context for the application to load.  If the
    user is not logged in, then they are redirected to the login choice page.
    """

    template_name = "agol_app/webApp.html"

    def get_context_data(self, **kwargs):
        try:
            context = super(AGOLApp, self).get_context_data(**kwargs)
            context['username'] = self.request.user.username
            context['access_token'] = self.request.user.user_profile.agol_token
            context['expires_at'] = self.request.user.user_profile.agol_expires_at
            context['app_id'] = settings.AGOL_OAUTH2_APP_ID
            context['portal_url'] = settings.AGOL_OAUTH2_PORTAL_URL
            context['default_map'] = settings.AGOL_START_MAP
            return context
        except:
            return dict()


