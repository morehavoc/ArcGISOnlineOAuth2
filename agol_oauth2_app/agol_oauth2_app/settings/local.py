from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CLASSES += (
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
#'debug_toolbar',
)


AGOL_OAUTH2_PORTAL_URL = r"https://www.arcgis.com"
AGOL_OAUTH2_APP_ID = ""
AGOL_OAUTH2_SECRET = ""
AGOL_OAUTH2_REDIRECT_URI = ""
AGOL_START_MAP = ""