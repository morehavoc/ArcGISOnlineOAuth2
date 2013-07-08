#ArcGISOnlineOAuth2

This example Django application demonstraits how an existing Javascript application can be altered to use OAuth2 security with very few changes to the Javascript itself.

This example uses backend OAuth authentication so that the user can also be authenticated on the server hosting this application.  This allows the application to store information about this user like preferences so that next time the user logs in those settings can be pulled from the database and used.

To get started, you will need to have some knowledge of Django.  

##Getting Started

1. Check the Requirments folder for Python libraries that you will need to install.  You can setup your own virtual environment and use pip to install the required libraries using:
```
pip install -r path/to/requirments/txt
```

2. Look in the ```agol_oauth2_app.settings.base``` file and update the following lines with your information:
```python
AGOL_OAUTH2_PORTAL_URL = r"https://www.arcgis.com"
AGOL_OAUTH2_APP_ID = ""
AGOL_OAUTH2_SECRET = ""
AGOL_OAUTH2_REDIRECT_URI = ""
AGOL_START_MAP = ""
```

3. Use the Django syncdb command to create the appropriate databae tables and a new user.

3. Use the Django runserver command, and visit the local page, you should be redirected to a login choice page where you can choose to login as the user you created in the previous step, or using your ArcGIS Online account.

If you have any questions, contact me via my website http://www.moravec.net or email via morehavoc[at]gmail[dot]com.
