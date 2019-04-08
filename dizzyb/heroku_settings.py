from dizzyb.settings import *
   # imports everything from the 'settings.py' file
import django_heroku

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
   # will prevent specific errors from showing to the production user

django_heroku.settings(locals())
   # locals returns a dictionary of all your local variables