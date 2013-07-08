from django.db import models
from django.conf import settings

class user_profile(models.Model):
    """
    A simple 1:1 helper table for the standard Django user model.  This will hold all of our AGOL tokens.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    agol_user = models.BooleanField()
    agol_token = models.CharField(max_length=1000)
    agol_refresh_token = models.CharField(max_length=1000)
    agol_expires_at = models.BigIntegerField()