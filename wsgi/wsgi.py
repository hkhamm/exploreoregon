import sys
import os
import os.path

# code dir is one level above us
APPS_DIR = "/var/www/map-app/code/apps"

# the env dir is one level above us
ENV_DIR = "/var/www/map-app/env"

# activate the virtualenv
activate_this = os.path.join(ENV_DIR, 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

# add the apps directory to the python path
sys.path.insert(0, APPS_DIR)


# load up django 
from django.core.management import execute_manager
from django.core.handlers.wsgi import WSGIHandler

# tell django to find settings at APPS_DIR/mainsite/settings.py'
os.environ['DJANGO_SETTINGS_MODULE'] = 'mainsite.settings'

# hand off to the wsgi application
application = WSGIHandler()
